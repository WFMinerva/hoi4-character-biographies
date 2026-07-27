from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
from typing import Iterable, Iterator

# CI runners default stdout to a legacy codepage; audit output is Chinese.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
# self_test.py sets CBIO_ROOT to redirect all checks at a synthetic fixture tree.
_override = os.environ.get("CBIO_ROOT")
if _override:
    ROOT = Path(_override).expanduser().resolve()
SOURCE_ROOTS = (ROOT / "src" / "shared", ROOT / "src" / "full_only")
TEXT_SUFFIXES = {".txt", ".yml", ".mod", ".md", ".json", ".csv", ".py", ".ps1"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def iter_source_files() -> Iterator[Path]:
    for base in SOURCE_ROOTS:
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.name != "AGENTS.md":
                yield p


def source_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


@dataclass(frozen=True)
class ScriptToken:
    value: str
    line: int
    quoted: bool = False


def lex_script(text: str) -> list[ScriptToken]:
    """Tokenize Paradox script while dropping comments and whitespace."""
    out: list[ScriptToken] = []
    i = 0
    line = 1
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in " \t\r":
            i += 1
            continue
        if ch == "\n":
            line += 1
            i += 1
            continue
        if ch == "#":
            j = text.find("\n", i)
            if j == -1:
                break
            i = j
            continue
        if ch in "{}=":
            out.append(ScriptToken(ch, line, False))
            i += 1
            continue
        if ch == '"':
            start_line = line
            j = i + 1
            escaped = False
            while j < n:
                c = text[j]
                if c == "\n":
                    line += 1
                if escaped:
                    escaped = False
                elif c == "\\":
                    escaped = True
                elif c == '"':
                    j += 1
                    break
                j += 1
            out.append(ScriptToken(text[i:j], start_line, True))
            i = j
            continue
        j = i
        while j < n and text[j] not in " \t\r\n{}=#\"":
            j += 1
        out.append(ScriptToken(text[i:j], line, False))
        i = j
    return out


def normalize_script_without_desc(text: str) -> list[str]:
    tokens = lex_script(text)
    result: list[str] = []
    i = 0
    while i < len(tokens):
        if (
            tokens[i].value == "desc"
            and i + 2 < len(tokens)
            and tokens[i + 1].value == "="
            and tokens[i + 2].value != "{"
        ):
            i += 3
            continue
        result.append(tokens[i].value)
        i += 1
    return result


def iter_desc_assignments(text: str):
    """Yield (line, value, ancestor block names) for scalar desc assignments."""
    tokens = lex_script(text)
    stack: list[str] = []
    i = 0
    while i < len(tokens):
        if i + 2 < len(tokens) and tokens[i + 1].value == "=" and tokens[i + 2].value == "{":
            stack.append(tokens[i].value)
            i += 3
            continue
        if tokens[i].value == "}":
            if stack:
                stack.pop()
            i += 1
            continue
        if (
            tokens[i].value == "desc"
            and i + 2 < len(tokens)
            and tokens[i + 1].value == "="
            and tokens[i + 2].value != "{"
        ):
            yield tokens[i].line, tokens[i + 2].value, tuple(stack)
            i += 3
            continue
        i += 1


def run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check
    )


def git_available() -> bool:
    if not (ROOT / ".git").exists():
        return False
    try:
        run_git(["rev-parse", "--is-inside-work-tree"])
        return True
    except Exception:
        return False


def resolve_diff_base(explicit: str | None = None) -> str | None:
    if not git_available():
        return None
    if explicit:
        run_git(["rev-parse", "--verify", explicit])
        return explicit
    env = os.environ.get("CBIO_DIFF_BASE")
    if env:
        run_git(["rev-parse", "--verify", env])
        return env
    branch = run_git(["branch", "--show-current"]).stdout.strip()
    if branch and branch != "main":
        try:
            run_git(["rev-parse", "--verify", "main"])
            return run_git(["merge-base", "HEAD", "main"]).stdout.strip()
        except Exception:
            pass
    try:
        tags = run_git(["tag", "--list", "*-stable", "--sort=-creatordate"]).stdout.splitlines()
        if tags:
            return tags[0].strip()
    except Exception:
        pass
    return "HEAD"


def changed_source_paths(base: str | None = None) -> list[str]:
    resolved = resolve_diff_base(base)
    if not resolved:
        return []
    cp = run_git(["diff", "--name-only", resolved, "--", "src"])
    paths = {x.strip().replace("\\", "/") for x in cp.stdout.splitlines() if x.strip()}
    untracked = run_git(["ls-files", "--others", "--exclude-standard", "--", "src"]).stdout.splitlines()
    paths.update(x.strip().replace("\\", "/") for x in untracked if x.strip())
    return sorted(paths)


def find_vanilla_reference() -> Path | None:
    env = os.environ.get("HOI4_VANILLA_PATH")
    if env:
        p = Path(env).expanduser()
        if p.exists():
            return p
    cfg = ROOT / "reference" / "vanilla_path.json"
    if cfg.exists():
        data = load_json(cfg)
        p = Path(data["path"]).expanduser()
        if p.exists():
            return p
    return None
