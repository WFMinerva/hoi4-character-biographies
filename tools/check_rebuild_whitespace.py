from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from common import ROOT, find_vanilla_reference, load_json, resolve_diff_base


def unauthorized_whitespace(root: Path, vanilla: Path, base: str, donor: Path | None = None) -> tuple[list[str], int]:
    diff = subprocess.run(
        ["git", "diff", "--check", base, "--", "src"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )
    errors: list[str] = []
    inherited = 0
    cache: dict[str, list[str]] = {}
    donor_cache: dict[str, list[str]] = {}
    for raw in diff.stdout.splitlines():
        match = re.match(r"^(.+?):(\d+): (trailing whitespace|space before tab in indent|new blank line at EOF)\.$", raw)
        if not match:
            continue
        rel, line_number, kind = match.group(1), int(match.group(2)), match.group(3)
        source = root / rel
        original = vanilla / rel.removeprefix("src/full_only/").removeprefix("src/shared/")
        if not original.exists():
            errors.append(f"非原版覆盖文件的空白告警: {rel}:{line_number} {kind}")
            continue
        if kind == "new blank line at EOF":
            if original.read_bytes().endswith(b"\n\n") and source.read_bytes().endswith(b"\n\n"):
                inherited += 1
            else:
                errors.append(f"新增文件尾空行: {rel}")
            continue
        if rel not in cache:
            cache[rel] = original.read_text(encoding="utf-8-sig").splitlines()
        donor_lines: list[str] = []
        if donor is not None and (donor / rel.removeprefix("src/full_only/").removeprefix("src/shared/")).exists():
            if rel not in donor_cache:
                donor_cache[rel] = (donor / rel.removeprefix("src/full_only/").removeprefix("src/shared/")).read_text(encoding="utf-8-sig").splitlines()
            donor_lines = donor_cache[rel]
        source_line = source.read_text(encoding="utf-8-sig").splitlines()[line_number - 1]
        if source_line in cache[rel] or source_line in donor_lines:
            inherited += 1
        else:
            errors.append(f"新增空白格式问题: {rel}:{line_number} {kind}: {source_line!r}")
    return errors, inherited


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base")
    args = parser.parse_args()
    if not (ROOT / "audit/allowlists/rebuild_manifest.json").exists():
        print("rebuild_whitespace: SKIP（无重建manifest）")
        return
    vanilla = find_vanilla_reference()
    if vanilla is None:
        raise SystemExit("ERROR 未配置原版路径")
    errors, inherited = unauthorized_whitespace(ROOT, vanilla, resolve_diff_base(args.base), Path(load_json(ROOT / "audit/allowlists/rebuild_manifest.json")["donor_path"]))
    for error in errors:
        print("ERROR", error)
    print(f"rebuild_whitespace: inherited={inherited} unauthorized={len(errors)}")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
