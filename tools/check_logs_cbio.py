#!/usr/bin/env python3
"""钢四人物小传MOD 实机日志判读工具（裁剪版）。

裁剪自《开局一键爽玩》tools/check_logs.py。本 MOD 无 OCS_TEST 自检机制，
故不实现标记铁律（等效于爽玩 --exempt-markers 常开，事实已在本工具头注明）；
白名单过滤、错误样口径、版本绑定、脱敏与 result.json 结构沿用其设计。

判定口径：
- error.log 全行白名单过滤；未命中白名单的行按「签名」聚合为新错误告警。
- text.log 非 0 字节 = 本地化错误签名告警（0 字节可表示未发现文本错误）。
- game.log 仅对「错误样」行（error/invalid/unknown/exception/failed/warning）
  告警，正常运行行忽略（运行日志口径）。
- setup.log 做加载摘要检查（存在性 + china_bio/CBIO 加载行计数），不过滤。
- code_revisions.log 版本绑定失败时降级人工登记（记入 result.json）。

用法：
    python tools/check_logs_cbio.py --logs <游戏日志目录> --round <轮次>
        [--out <result.json>]

输出（按 tools/AGENTS.md 输出边界）：默认 audit/reports/cbio_result.json；
失败返回非零退出码。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# 与仓库既有工具一致：强制 UTF-8 stdout，避免 Windows 控制台 charmap 编码错误
# （先例：2026-07-28「tools: force utf-8 stdout for CI runners」）。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
WHITELIST_PATH = ROOT / "tools" / "cbio_log_whitelist.json"

FILTERED_LOGS = ("error.log", "game.log", "text.log")
SETUP_LOG = "setup.log"
VERSION_LOG = "code_revisions.log"

TIME_PREFIX_RE = re.compile(r"^\[[^\]]*\]\[[^\]]*\]\[[^\]]*\]:\s*")
ERROR_LIKE_RE = re.compile(r"\b(error|invalid|unknown|exception|failed|warning)\b", re.IGNORECASE)
CBIO_LINE_RE = re.compile(r"china_bio|CBIO", re.IGNORECASE)


def _read_lines(path: Path) -> list[str]:
    """Read a log file line by line; tolerate missing files and bad encodings."""
    if not path.is_file():
        return []
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def load_whitelist(path: Path = WHITELIST_PATH) -> list[dict]:
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"[FAIL] 白名单文件不可读或格式错误：{path}（{exc}）") from exc
    if data.get("schema_version") != 1:
        raise SystemExit(f"白名单文件 schema_version 不支持：{data.get('schema_version')}")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise SystemExit(f"[FAIL] 白名单文件缺少 entries 列表：{path}")
    return entries


def whitelist_for_log(entries: list[dict], log_name: str) -> list[dict]:
    return [e for e in entries if e.get("log") == log_name]


def _line_matches(entry: dict, line: str) -> bool:
    pattern = entry["pattern"]
    if entry.get("regex"):
        return re.search(pattern, line) is not None
    return pattern in line


def _redact_identity(text: str) -> str:
    """归档防泄漏：替换本机用户目录/机器名（含正反斜杠路径变体）。

    用户名只在路径形态（C:/Users/<name>）下替换，避免误伤正文中的普通单词；
    引擎报错常见 `C:\\Users\\<名>\\...` 形态，两种分隔符都覆盖。
    """
    for raw in (os.environ.get("USERPROFILE"), os.environ.get("COMPUTERNAME")):
        if raw:
            text = text.replace(raw, "<REDACTED>")
            text = text.replace(raw.replace("\\", "/"), "<REDACTED>")
    user = os.environ.get("USERNAME")
    if user:
        text = text.replace(f"C:/Users/{user}", "C:/Users/<REDACTED>")
        text = text.replace(f"C:\\Users\\{user}", "C:\\Users\\<REDACTED>")
    return text


def _signature(line: str) -> str:
    """Normalize a log line to a stable signature for grouping.

    去掉时间前缀，并把引擎报错的行号（line : 54 等）归一为 line : <N>，使同一
    错误类型的不同位置报告聚合为一类新签名。
    """
    sig = TIME_PREFIX_RE.sub("", line).strip()
    sig = re.sub(r"line\s*:\s*\d+", "line : <N>", sig)
    return sig


def filter_log(lines: list[str], entries: list[dict], mode: str = "all") -> dict:
    """Return whitelist-filtering result for one log.

    mode="all"：未命中白名单的行全部计为新签名（error.log/text.log 用）；
    mode="error_like"：仅「错误样」行计为新签名，正常运行行忽略（game.log 用）。
    """
    matched = 0
    unmatched: dict[str, dict] = {}
    for line in lines:
        if not line.strip():
            continue
        line = _redact_identity(line)
        if any(_line_matches(e, line) for e in entries):
            matched += 1
            continue
        if mode == "error_like" and not ERROR_LIKE_RE.search(line):
            continue
        sig = _signature(line)
        bucket = unmatched.setdefault(sig, {"count": 0, "sample": line[:400]})
        bucket["count"] += 1
    return {"total_lines": len(lines), "whitelisted": matched, "unmatched": unmatched}


def read_game_version(logs_dir: Path) -> dict:
    """Bind the game build from code_revisions.log; degrade to manual note on failure."""
    path = logs_dir / VERSION_LOG
    data: dict[str, str] = {}
    for line in _read_lines(path):
        if ":" in line:
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip()
    if data.get("game_hash_short"):
        return {
            "source": VERSION_LOG,
            "game_hash_short": data["game_hash_short"],
            "game_timestamp": data.get("game_timestamp", ""),
            "manual_fallback": False,
        }
    return {
        "source": "manual",
        "game_hash_short": "",
        "game_timestamp": "",
        "manual_fallback": True,
        "note": "code_revisions.log 缺失或解析失败，需人工登记游戏版本号",
    }


def summarize_setup_log(lines: list[str]) -> dict:
    """Load-summary check for setup.log (load log; every line is a normal record)."""
    cbio_lines = sum(1 for line in lines if CBIO_LINE_RE.search(line))
    return {"exists": bool(lines), "total_lines": len(lines), "cbio_lines": cbio_lines}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="实机日志判读（钢四人物小传裁剪版）：白名单过滤＋版本绑定＋result.json")
    parser.add_argument("--logs", type=Path, required=True,
                        help="游戏日志目录（Documents\\Paradox Interactive\\Hearts of Iron IV\\logs）")
    parser.add_argument("--round", default="", help="轮次标识（如 v130e-test1）")
    parser.add_argument("--out", type=Path, default=None,
                        help="result.json 输出路径（默认 audit/reports/cbio_result.json）")
    args = parser.parse_args(argv)

    logs_dir = args.logs
    if not logs_dir.is_dir():
        print(f"[FAIL] 日志目录不存在：{logs_dir}", file=sys.stderr)
        return 2

    lines_by_log = {name: _read_lines(logs_dir / name) for name in (*FILTERED_LOGS, SETUP_LOG)}
    entries = load_whitelist()

    filter_results = {}
    clean = True
    new_signatures: list[dict] = []
    modes = {"game.log": "error_like", "error.log": "all", "text.log": "all"}
    for log_name in FILTERED_LOGS:
        result = filter_log(lines_by_log[log_name], whitelist_for_log(entries, log_name),
                            mode=modes[log_name])
        filter_results[log_name] = result
        if result["unmatched"]:
            clean = False
            for sig, bucket in sorted(result["unmatched"].items()):
                new_signatures.append({"log": log_name, "signature": sig,
                                       "count": bucket["count"], "sample": bucket["sample"]})

    version = read_game_version(logs_dir)
    setup = summarize_setup_log(lines_by_log[SETUP_LOG])

    verdict = "PASS"
    reasons: list[str] = []
    if not clean:
        verdict = "FAIL"
        reasons.append(f"日志存在白名单外的新错误签名 {len(new_signatures)} 类")
    if not setup["exists"]:
        reasons.append("[警告] setup.log 不存在")
    else:
        reasons.append(f"setup.log 存在：{setup['total_lines']} 行，china_bio/CBIO 加载行 {setup['cbio_lines']} 行")
    if not reasons or (len(reasons) == 1 and reasons[0].startswith("[警告]")):
        if not reasons:
            reasons.append("白名单过滤干净")
    reasons.append("标记铁律不适用：本 MOD 无 OCS_TEST 自检机制（裁剪版口径，见工具头注释）")

    result = {
        "schema_version": 1,
        "round": args.round,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "logs_dir": _redact_identity(str(logs_dir)),
        "game_version": version,
        "whitelist": {"clean": clean, "new_signatures": new_signatures},
        "markers": {"note": "本 MOD 无 OCS_TEST 自检机制，标记判定不适用"},
        "setup_log": setup,
        "verdict": verdict,
        "verdict_reasons": reasons,
    }

    out_path = args.out or (ROOT / "audit" / "reports" / "cbio_result.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== 实机日志判读摘要（钢四裁剪版） ===")
    print(f"轮次: {args.round or '(未指定)'}  日志目录: {_redact_identity(str(logs_dir))}")
    print(f"游戏版本: {version.get('game_hash_short') or '(需人工登记)'}"
          + ("" if not version.get("manual_fallback") else "  [绑定失败，降级人工登记]"))
    print(f"白名单过滤: {'干净' if clean else '发现新错误签名 ' + str(len(new_signatures)) + ' 类'}")
    for item in new_signatures[:10]:
        print(f"  - [{item['log']}] x{item['count']} {item['signature'][:120]}")
    print(f"setup.log: {'存在（' + str(setup['total_lines']) + ' 行，CBIO 加载 ' + str(setup['cbio_lines']) + ' 行）' if setup['exists'] else '不存在（警告）'}")
    print(f"判定: {verdict}  理由: {'；'.join(reasons)}")
    print(f"结果已写入: {out_path}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
