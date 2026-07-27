"""Canary tests for the audit checks themselves.

For every check: build a synthetic fixture tree (CBIO_ROOT redirect), assert
the check passes on the pristine fixture, then inject one deliberate fault
and assert the check fails. A check that cannot catch its own canary is
reported here before it can silently weaken the daily audit gate.

check_diff_whitelist.py and compare_with_vanilla.py are out of scope: they
require a git history and the vanilla game files respectively.
"""
from __future__ import annotations

import os
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


def run(script: str, fixture: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, CBIO_ROOT=str(fixture))
    return subprocess.run(
        [sys.executable, str(TOOLS / script)], cwd=fixture, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
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


def fault_snapshot_version(fx: Path) -> None:
    p = fx / "AGENTS.md"
    text = p.read_text(encoding="utf-8-sig")
    assert "v130d" in text
    p.write_text(text.replace("v130d-stable", "v129x-stable", 1), encoding="utf-8")


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


CASES = [
    ("check_encoding.py", fault_strip_bom),
    ("check_localisation.py", fault_duplicate_key),
    ("check_aliases.py", fault_alias_missing_target),
    ("check_text_quality.py", fault_text_residue),
    ("check_human_decisions.py", fault_delete_protected),
    ("check_human_decisions.py", fault_ledger_parity),
    ("check_snapshot.py", fault_snapshot_version),
    ("check_script_structure.py", fault_unbalanced_brace),
    ("check_desc_semantics.py", fault_desc_wrong_level),
]

failures = []
with tempfile.TemporaryDirectory(prefix="cbio_selftest_") as tmp:
    for script, fault in CASES:
        fx = Path(tmp) / (script.replace(".py", "") + "_" + fault.__name__)
        build_fixture(fx)
        clean = run(script, fx)
        if clean.returncode != 0:
            failures.append(f"{script}: 干净fixture未通过\n{clean.stdout[-800:]}")
            continue
        fault(fx)
        dirty = run(script, fx)
        status = "OK" if dirty.returncode != 0 else "MISS"
        print(f"{status}  {script} + {fault.__name__}: 干净=通过, 故障={'拦截' if dirty.returncode != 0 else '漏检!'}")
        if dirty.returncode == 0:
            failures.append(f"{script}: 未能拦截注入故障 {fault.__name__}")

print(f"\nself_test: cases={len(CASES)} failures={len(failures)} (check_diff_whitelist/compare_with_vanilla 不在金丝雀范围)")
for f in failures:
    print("FAIL", f)
raise SystemExit(1 if failures else 0)
