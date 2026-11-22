from __future__ import annotations

import argparse
from collections import Counter
import re
import subprocess
from pathlib import Path

from common import ROOT, changed_source_paths, find_vanilla_reference, load_json, resolve_diff_base, sha256_bytes
from rebase_evidence import baseline_game_version, load_rebase_document, rebase_version, validated_rebases


def unauthorized_whitespace(
    root: Path, vanilla: Path, base: str, donor: Path | None = None,
    rebases: set[str] | None = None, approved_lines: Counter | None = None,
) -> tuple[list[str], int]:
    diff = subprocess.run(
        ["git", "-c", "core.quotePath=false", "diff", "--check", base, "--", "src"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )
    errors: list[str] = []
    if diff.returncode not in {0, 2}:
        return [f"无法检查 Git 空白: {diff.stdout.strip()}"], 0
    rebases = rebases or set()
    remaining = Counter(approved_lines or {})
    inherited = 0
    cache: dict[str, list[str]] = {}
    donor_cache: dict[str, list[str]] = {}
    output = diff.stdout.splitlines()
    if rebases:
        untracked = subprocess.check_output(
            ["git", "-c", "core.quotePath=false", "ls-files", "--others", "--exclude-standard", "-z", "--", "src"],
            cwd=root, encoding="utf-8",
        )
        for path in (p for p in untracked.split("\0") if p):
            new = subprocess.run(
                ["git", "-c", "core.quotePath=false", "diff", "--no-index", "--check", "--", "/dev/null", path],
                cwd=root, capture_output=True, encoding="utf-8",
            )
            if new.returncode not in {0, 1, 2, 3}:
                errors.append(f"无法检查新文件空白: {path}: {new.stderr.strip()}")
            output.extend(new.stdout.splitlines())
    for raw in output:
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
            continue
        exception = (rel, kind, sha256_bytes(source_line.encode("utf-8")))
        if rel in rebases and remaining[exception] > 0:
            remaining[exception] -= 1
            continue
        errors.append(f"新增空白格式问题: {rel}:{line_number} {kind}: {source_line!r}")
    errors.extend(f"历史包空白例外未命中: {key} ×{count}" for key, count in remaining.items() if count)
    return errors, inherited


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base")
    args = parser.parse_args()
    manifest = ROOT / "audit/allowlists/rebuild_manifest.json"
    document = load_rebase_document()
    candidate = rebase_version(document)
    if not manifest.exists() and not candidate:
        print("rebuild_whitespace: SKIP（无重建manifest）")
        return
    vanilla = find_vanilla_reference()
    if vanilla is None:
        raise SystemExit("ERROR 未配置原版路径")
    historical = load_json(manifest) if manifest.exists() else {}
    version = candidate or baseline_game_version()
    use_historical = historical and not candidate and version in (None, historical.get('game_version'))
    donor = Path(historical['donor_path']) if use_historical else None
    base = resolve_diff_base(args.base)
    verified, rebase_errors = validated_rebases(base, changed_source_paths(args.base), document.get("exceptions", []))
    approved = Counter((row["path"], row["kind"], row["line_sha256"]) for row in document.get("released_whitespace", []))
    errors, inherited = unauthorized_whitespace(ROOT, vanilla, base, donor, set(verified), approved)
    errors.extend(rebase_errors)
    for error in errors:
        print("ERROR", error)
    print(f"rebuild_whitespace: inherited={inherited} released_exceptions={sum(approved.values())} unauthorized={len(errors)}")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
