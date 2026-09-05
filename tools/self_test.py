"""Canary tests for the audit checks themselves.

For every check: build a synthetic fixture tree (CBIO_ROOT redirect), assert
the check passes on the pristine fixture, then inject one deliberate fault
and assert the check fails. A check that cannot catch its own canary is
reported here before it can silently weaken the daily audit gate.

Git-backed and vanilla-backed checks receive synthetic dependencies inside
their fixture, so every daily checker has at least one canary.
"""
from __future__ import annotations

import os
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# CI runners default stdout to a legacy codepage; this script prints Chinese.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REAL_ROOT = Path(__file__).resolve().parents[1]
TOOLS = REAL_ROOT / "tools"

COPY_PATHS = [
    "src",
    "audit/baselines/encoding_baseline.json",
    "workbench/decisions/human_decisions.json",
    "docs/HUMAN_DECISIONS.md",
    "docs/CURRENT_BASELINE.md",
    "AGENTS.md",
]


def build_fixture(dst: Path) -> None:
    for rel in COPY_PATHS:
        src = REAL_ROOT / rel
        target = dst / rel
        if src.is_dir():
            shutil.copytree(src, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)


def run(script: str, fixture: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, CBIO_ROOT=str(fixture))
    return subprocess.run(
        [sys.executable, str(TOOLS / script), *args], cwd=fixture, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )


def git(fixture: Path, *args: str) -> None:
    result = subprocess.run(
        ["git", *args], cwd=fixture, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        raise AssertionError(f"fixture Git命令失败: git {' '.join(args)}\n{result.stdout}")


def setup_git_fixture(fx: Path) -> None:
    git(fx, "init")
    git(fx, "config", "user.email", "selftest@example.invalid")
    git(fx, "config", "user.name", "CBIO self-test")
    git(fx, "add", ".")
    git(fx, "commit", "-m", "pristine fixture")


def setup_vanilla_fixture(fx: Path) -> None:
    vanilla = fx / "reference" / "vanilla"
    shutil.copytree(fx / "src" / "full_only", vanilla)
    (fx / "reference").mkdir(parents=True, exist_ok=True)
    (fx / "reference" / "vanilla_path.json").write_text(
        json.dumps({"path": str(vanilla)}, ensure_ascii=False),
        encoding="utf-8",
    )


def setup_cbio_logs(fx: Path) -> None:
    """合成日志fixture：全部行均命中白名单（干净用例）。"""
    logs = fx / "synthetic_logs"
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "error.log").write_text(
        "[15:00:41][no_game_date][virtualfilesystem_physfs.cpp:1260]: Error setting buffer for file: gfx/models/units/planes/fighter_1_kamikaze.mesh. File may not read/write correctly.\n"
        "[15:01:13][no_game_date][gfx_dx11.cpp:84]: Failed to create 2D texture (format=87, mips=1: Not enough memory resources are available to complete this operation.\n"
        " (0x8007000e)\n"
        "[15:02:30][1936.01.01.12][gamelobby.cpp:1779]: Exception in: remotefile.cpp, line: 238. Description: Failed allocate data buffer.\n",
        encoding="utf-8",
    )
    (logs / "game.log").write_text(
        "[15:02:40][1936.01.01.12][frontend.cpp:682]: Launching SINGLEPLAYER-game\nConflict Risk detected\n",
        encoding="utf-8",
    )
    (logs / "setup.log").write_text("[load] china_bio shared file loaded\n", encoding="utf-8")
    (logs / "code_revisions.log").write_text(
        "game_hash_short: a729d47bd\ngame_timestamp: 2026-06-29 15:17:03 +0200\n",
        encoding="utf-8",
    )


def cbio_logs_args(fx: Path) -> list[str]:
    return ["--logs", str(fx / "synthetic_logs"), "--out", str(fx / "cbio_result.json")]


def fault_cbio_new_signature(fx: Path) -> None:
    """注入白名单外的错误签名行，判读工具必须拦截（FAIL）。"""
    p = fx / "synthetic_logs" / "error.log"
    p.write_text(
        p.read_text(encoding="utf-8")
        + "\n[16:00:00][1936.01.01.12][selftest.cpp:1]: CBIO selftest injected unknown error\n",
        encoding="utf-8",
    )


def first_file(fixture: Path, pattern: str) -> Path:
    for p in sorted((fixture / "src").rglob(pattern)):
        if p.is_file() and p.name != "AGENTS.md":
            return p
    raise AssertionError(f"fixture缺少文件: {pattern}")


def rewrite_keep_bom(path: Path, transform) -> None:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    out = transform(text)
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + out.encode("utf-8"))


# --- fault injectors: each takes the fixture root and breaks exactly one rule ---

def fault_strip_bom(fx: Path) -> None:
    p = None
    for cand in sorted(fx.joinpath("src").rglob("*.yml")):
        if "localisation" in cand.relative_to(fx).as_posix().split("/"):
            p = cand
            break
    assert p is not None, "fixture缺少本地化yml"
    raw = p.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf"), f"目标yml无BOM，故障注入无效: {p}"
    p.write_bytes(raw[3:])


def fault_duplicate_key(fx: Path) -> None:
    p = next(fx.joinpath("src").rglob("*.yml"))
    def add(text: str) -> str:
        for line in text.splitlines():
            if ':"' in line or ('"' in line and ":" in line):
                return text + "\n" + line + "\n"
        raise AssertionError("找不到可复制key行")
    rewrite_keep_bom(p, add)


def fault_alias_missing_target(fx: Path) -> None:
    p = next(fx.joinpath("src").rglob("*.yml"))
    rewrite_keep_bom(p, lambda t: t + '\n CBIO_selftest_alias_desc:0 "$CBIO_no_such_target$"\n')


def fault_text_residue(fx: Path) -> None:
    p = next(fx.joinpath("src").rglob("*.yml"))
    rewrite_keep_bom(p, lambda t: t + '\n CBIO_selftest_residue_desc:0 "§Y残留测试"\n')


def fault_delete_protected(fx: Path) -> None:
    target = fx / "src/full_only/history/countries/EGY - Egypt.txt"
    assert target.exists(), "fixture缺少受保护文件"
    target.unlink()


def fault_ledger_parity(fx: Path) -> None:
    p = fx / "docs/HUMAN_DECISIONS.md"
    text = p.read_text(encoding="utf-8-sig")
    assert "SIK_chiang_yufen_desc" in text
    p.write_text(text.replace("SIK_chiang_yufen_desc", "SIK_removed_desc"), encoding="utf-8")


def fault_ledger_reverse_parity(fx: Path) -> None:
    p = fx / "docs/HUMAN_DECISIONS.md"
    text = p.read_text(encoding="utf-8-sig")
    p.write_text(text + "\n<!-- ledger:rule:not_in_json status=confirmed -->\n", encoding="utf-8")


def fault_ledger_marker_missing(fx: Path) -> None:
    p = fx / "docs/HUMAN_DECISIONS.md"
    text = p.read_text(encoding="utf-8-sig")
    marker = "<!-- ledger:rule:project_pure_bio status=confirmed -->"
    assert marker in text
    p.write_text(text.replace(marker, "", 1), encoding="utf-8")


def fault_snapshot_pointer_missing(fx: Path) -> None:
    p = fx / "AGENTS.md"
    text = p.read_text(encoding="utf-8-sig")
    assert "docs/CURRENT_BASELINE.md" in text
    p.write_text(text.replace("docs/CURRENT_BASELINE.md", "docs/BASELINE_ARCHIVE.md"), encoding="utf-8")


def fault_snapshot_version_reembedded(fx: Path) -> None:
    p = fx / "AGENTS.md"
    text = p.read_text(encoding="utf-8-sig")
    p.write_text(text + "\n当前版本：v999-test\n", encoding="utf-8")


def fault_unbalanced_brace(fx: Path) -> None:
    p = first_file(fx, "*.txt")
    p.write_bytes(p.read_bytes() + b"\nselftest = {\n")


def fault_desc_wrong_level(fx: Path) -> None:
    char_dir = fx / "src/shared/common/characters"
    p = sorted(char_dir.rglob("*.txt"))[0]
    def inject(text: str) -> str:
        i = text.index("characters")
        j = text.index("{", i)
        return text[: j + 1] + "\n    desc = CBIO_selftest\n" + text[j + 1:]
    rewrite_keep_bom(p, inject)


def fault_forbidden_diff(fx: Path) -> None:
    p = sorted((fx / "src/shared").rglob("*.txt"))[0]
    rewrite_keep_bom(p, lambda t: t + "\nideology = fascism\n")


def fault_vanilla_semantics(fx: Path) -> None:
    p = sorted((fx / "src/full_only").rglob("*.txt"))[0]
    rewrite_keep_bom(p, lambda t: t + "\nideology = fascism\n")


CASES = [
    ("check_encoding.py", fault_strip_bom, None, None),
    ("check_localisation.py", fault_duplicate_key, None, None),
    ("check_aliases.py", fault_alias_missing_target, None, None),
    ("check_text_quality.py", fault_text_residue, None, None),
    ("check_human_decisions.py", fault_delete_protected, None, None),
    ("check_human_decisions.py", fault_ledger_parity, None, None),
    ("check_human_decisions.py", fault_ledger_reverse_parity, None, None),
    ("check_human_decisions.py", fault_ledger_marker_missing, None, None),
    ("check_snapshot.py", fault_snapshot_pointer_missing, None, None),
    ("check_snapshot.py", fault_snapshot_version_reembedded, None, None),
    ("check_script_structure.py", fault_unbalanced_brace, None, None),
    ("check_desc_semantics.py", fault_desc_wrong_level, None, None),
    ("check_diff_whitelist.py", fault_forbidden_diff, setup_git_fixture, None),
    ("compare_with_vanilla.py", fault_vanilla_semantics, setup_vanilla_fixture, None),
    ("check_logs_cbio.py", fault_cbio_new_signature, setup_cbio_logs, cbio_logs_args),
]

failures = []
with tempfile.TemporaryDirectory(prefix="cbio_selftest_") as tmp:
    for script, fault, setup, args_fn in CASES:
        fx = Path(tmp) / (script.replace(".py", "") + "_" + fault.__name__)
        build_fixture(fx)
        if setup:
            setup(fx)
        extra = args_fn(fx) if args_fn else []
        clean = run(script, fx, *extra)
        if clean.returncode != 0:
            failures.append(f"{script}: 干净fixture未通过\n{clean.stdout[-800:]}")
            continue
        fault(fx)
        dirty = run(script, fx, *extra)
        status = "OK" if dirty.returncode != 0 else "MISS"
        print(f"{status}  {script} + {fault.__name__}: 干净=通过, 故障={'拦截' if dirty.returncode != 0 else '漏检!'}")
        if dirty.returncode == 0:
            failures.append(f"{script}: 未能拦截注入故障 {fault.__name__}")

print(f"\nself_test: cases={len(CASES)} failures={len(failures)}")
for f in failures:
    print("FAIL", f)
raise SystemExit(1 if failures else 0)
