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
import zipfile
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


def fault_snapshot_version(fx: Path) -> None:
    p = fx / "AGENTS.md"
    text = p.read_text(encoding="utf-8-sig")
    assert "v130e" in text
    p.write_text(text.replace("v130e-stable", "v130e2-stable", 1), encoding="utf-8")


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


def fault_unused_exact_exception(fx: Path) -> None:
    p = fx / "audit/allowlists/diff_exceptions.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"exceptions": [{
        "path": "src/full_only/events/never.txt",
        "approved_by_user": True,
        "exact_lines": [{"direction": "+", "line": "ideology = fascism", "count": 1}],
    }]}), encoding="utf-8")


def fault_vanilla_semantics(fx: Path) -> None:
    p = sorted((fx / "src/full_only").rglob("*.txt"))[0]
    rewrite_keep_bom(p, lambda t: t + "\nideology = fascism\n")


def setup_build_fixture(fx: Path) -> None:
    for target in ("lite", "full"):
        packaging = fx / "packaging" / target
        packaging.mkdir(parents=True)
        (packaging / "descriptor.mod").write_text('name="old"\npath="mod/old"\n', encoding="utf-8")
        (packaging / "outer.mod").write_text('name="old"\npath="mod/old"\n', encoding="utf-8")
    (fx / "src/shared/common/characters").mkdir(parents=True, exist_ok=True)
    (fx / "src/shared/common/characters/TST.txt").write_text("characters = { }\n", encoding="utf-8")
    (fx / "src/full_only/events").mkdir(parents=True, exist_ok=True)
    (fx / "src/full_only/events/TST.txt").write_text("country_event = { }\n", encoding="utf-8")
    built = run("build_release.py", fx, "--version", "selftest")
    assert built.returncode == 0, built.stdout


def build_version_args(fx: Path) -> list[str]:
    return ["--version", "selftest"]


def fault_zip_tamper(fx: Path) -> None:
    with zipfile.ZipFile(fx / "releases/china_bio_selftest.zip", "a") as archive:
        archive.writestr("china_bio_selftest/injected.txt", "not allowed")


def fault_zip_duplicate(fx: Path) -> None:
    with zipfile.ZipFile(fx / "releases/china_bio_selftest.zip", "a") as archive:
        archive.writestr("china_bio_selftest/descriptor.mod", "duplicate")


def test_verify_build_semantics() -> None:
    import hashlib
    import verify_build

    with tempfile.TemporaryDirectory(prefix="cbio_semantic_") as tmp:
        root = Path(tmp)
        source = root / "src/shared/TST.txt"
        source.parent.mkdir(parents=True)
        source.write_text("actual", encoding="utf-8")
        rows = {"src/shared/TST.txt": "self-consistent-but-wrong"}
        payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
        document = {
            "files": [{"path": "src/shared/TST.txt", "expected_sha256": "self-consistent-but-wrong"}],
            "unchanged": [],
            "semantic_manifest_sha256": hashlib.sha256(payload).hexdigest(),
        }
        path = root / "semantic.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        old_root = verify_build.ROOT
        try:
            verify_build.ROOT = root
            try:
                verify_build.semantic_manifest_check(path)
                raise AssertionError("语义清单与源码不符时必须失败")
            except ValueError:
                pass
        finally:
            verify_build.ROOT = old_root
    print("OK  verify_build.py: 语义清单-源码绑定自检通过")


def test_rebuild_overlay() -> None:
    from rebuild_with_vanilla import build_expected, output_bytes

    donor = """country_event = {
 id = selftest.1
 option = {
  create_country_leader = {
   desc = CBIO_selftest_desc
   ideology = anarchism
  }
 }
}
"""
    vanilla = donor.replace("   desc = CBIO_selftest_desc\n", "")
    expected, overlays, errors = build_expected("selftest.txt", donor, vanilla, {"desc"}, {"CBIO_selftest_desc"}, False, [])
    assert not errors, errors
    assert expected is not None and "desc = CBIO_selftest_desc" in expected
    assert overlays[0]["root"] == "selftest.1"

    bad, _, errors = build_expected("selftest.txt", donor.replace("selftest.1", "selftest.2").replace("ideology = anarchism", "ideology = fascism"), vanilla, {"desc"}, {"CBIO_selftest_desc"}, False, [])
    assert bad is None and errors, "未匹配人物desc必须失败"

    static_donor = donor.replace("CBIO_selftest_desc", '"POLITICS_ANARCHIST_COMMUNE_DESC"')
    static_vanilla = vanilla.replace("create_country_leader = {", "promote_character = {\n   character = SPR_anarchist_commune")
    _, requests, errors = build_expected("selftest.txt", static_donor, static_vanilla, {"desc"}, set(), False, [])
    assert not errors and requests[0]["action"] == "inherit_static", errors
    character_vanilla = "characters = {\n SPR_anarchist_commune = {\n  country_leader = {\n   ideology = anarchism\n  }\n }\n}\n"
    expected, overlays, errors = build_expected("SPR.txt", "characters = { }\n", character_vanilla, {"desc", "name"}, set(), True, requests)
    assert not errors and expected is not None and 'desc = "POLITICS_ANARCHIST_COMMUNE_DESC"' in expected, errors
    assert output_bytes("x\ny\n", b"\xef\xbb\xbfx\r\ny\r\n") == b"\xef\xbb\xbfx\r\ny\r\n"
    print("OK  rebuild_with_vanilla.py: 注入/未匹配/静态继承/BOM-EOL 自检通过")


def test_rebuild_whitespace() -> None:
    from check_rebuild_whitespace import unauthorized_whitespace

    with tempfile.TemporaryDirectory(prefix="cbio_whitespace_") as tmp:
        root = Path(tmp) / "repo"
        source = root / "src/full_only/events/TST.txt"
        original = root / "vanilla/events/TST.txt"
        source.parent.mkdir(parents=True)
        original.parent.mkdir(parents=True)
        source.write_text("a = 1\n", encoding="utf-8")
        git(root, "init")
        git(root, "config", "user.email", "selftest@example.invalid")
        git(root, "config", "user.name", "CBIO self-test")
        git(root, "add", ".")
        git(root, "commit", "-m", "base")
        source.write_text("a = 1 \n", encoding="utf-8")
        original.write_text("a = 1 \n", encoding="utf-8")
        errors, inherited = unauthorized_whitespace(root, root / "vanilla", "HEAD")
        assert not errors and inherited == 1, (errors, inherited)
        source.write_text("a = 1 \nnew = 2 \n", encoding="utf-8")
        errors, _ = unauthorized_whitespace(root, root / "vanilla", "HEAD")
        assert errors, "新增非原版空白必须拦截"
    print("OK  check_rebuild_whitespace.py: 原版继承/新增空白自检通过")


def test_rebuild_restore() -> None:
    from rebuild_with_vanilla import file_digest

    with tempfile.TemporaryDirectory(prefix="cbio_restore_") as tmp:
        root = Path(tmp)
        target = root / "src/shared/TST.txt"
        backup = root / "build/rebuild-backup/src/shared/TST.txt"
        created = root / "audit/allowlists/rebuild_manifest.json"
        backup.parent.mkdir(parents=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        created.parent.mkdir(parents=True)
        backup.write_text("original", encoding="utf-8")
        target.write_text("written", encoding="utf-8")
        created.write_text("created", encoding="utf-8")
        manifest = root / "build/rebuild-backup/manifest.json"
        manifest.write_text(json.dumps({
            "files": [{"target": "src/shared/TST.txt", "backup": "build/rebuild-backup/src/shared/TST.txt", "original_sha256": file_digest(backup), "written_sha256": file_digest(target)}],
            "created": [{"target": "audit/allowlists/rebuild_manifest.json", "sha256": file_digest(created)}],
        }), encoding="utf-8")
        clean = run("rebuild_with_vanilla.py", root, "--restore")
        assert clean.returncode == 0, clean.stdout
        assert target.read_text(encoding="utf-8") == "original" and not created.exists()
        target.write_text("other edit", encoding="utf-8")
        created.write_text("created", encoding="utf-8")
        dirty = run("rebuild_with_vanilla.py", root, "--restore")
        assert dirty.returncode != 0, "目标被其他改动污染时必须拒绝恢复"
        target.write_text("written", encoding="utf-8")
        backup.write_text("corrupt backup", encoding="utf-8")
        dirty = run("rebuild_with_vanilla.py", root, "--restore")
        assert dirty.returncode != 0 and target.read_text(encoding="utf-8") == "written", "备份损坏时必须先拒绝且不得覆盖目标"
    print("OK  rebuild_with_vanilla.py --restore: 哈希恢复/污染拦截自检通过")


def test_character_identity() -> None:
    from rebuild_with_vanilla import build_expected, parse_script, role_identity

    people = [
        ("RAJ_mahatma_mohandas_gandhi", "CBIO_RAJ_mahatma_mohandas_gandhi_desc"),
        ("RAJ_GOE_muhammad_ali_jinnah", "CBIO_RAJ_GOE_muhammad_ali_jinnah_desc"),
        ("RAJ_louis_mountbatten", "CBIO_RAJ_louis_mountbatten_desc"),
    ]
    donor_parts = ["country_event = {\n id = GOE_RAJ_partition.7\n"]
    for index, (character, key) in enumerate(people):
        donor_parts.append(f" option = {{\n  add_country_leader_role = {{\n   character = {character}\n   country_leader = {{\n    desc = {key}\n    ideology = liberalism\n    traits = {{ }}\n   }}\n  }}\n }}\n")
        if index == 0:
            donor_parts.append(" country_event = { id = GOE_RAJ_partition.8\n  option = { name = nested.option }\n }\n")
    donor_parts.append("}\n")
    donor = "".join(donor_parts)
    vanilla = donor.replace("    desc = CBIO_RAJ_mahatma_mohandas_gandhi_desc\n", "").replace("    desc = CBIO_RAJ_GOE_muhammad_ali_jinnah_desc\n", "").replace("    desc = CBIO_RAJ_louis_mountbatten_desc\n", "")
    gandhi = people[0][0]
    start = vanilla.index(f"  add_country_leader_role = {{\n   character = {gandhi}")
    end = vanilla.index(" option = {", start)
    vanilla = vanilla[:start] + f"  promote_character = {{\n   character = {gandhi}\n   ideology = liberalism\n  }}\n" + vanilla[end:]
    expected, overlays, errors = build_expected("GOE_Raj.txt", donor, vanilla, {"desc"}, {key for _, key in people}, False, [])
    assert not errors, errors
    assert sum(o["action"] == "inherit_static" and o["person_id"] == gandhi for o in overlays) == 1
    for character, key in people[1:]:
        blocks = [b for b in parse_script(expected, {"desc"}).blocks if b.container == "country_leader" and role_identity(expected, b.line).get("character") == character]
        assert len(blocks) == 1, (character, blocks)
        parsed = parse_script(expected, {"desc"})
        assert any(a.anchor == blocks[0].anchor and a.value == key for a in parsed.assignments), f"{character}错挂或漏挂"
        overlay = next(o for o in overlays if o["value"] == key)
        assert overlay["root"] == "GOE_RAJ_partition.7" and overlay["identity"]["character"] == character
    requests = [o for o in overlays if o["action"] == "inherit_static"]
    character_vanilla = f"characters = {{\n {gandhi} = {{\n  instance = {{\n   country_leader = {{\n    desc = {people[0][1]}\n    ideology = liberalism\n   }}\n  }}\n }}\n}}\n"
    _, shared_overlays, errors = build_expected("RAJ.txt", "characters = { }\n", character_vanilla, {"desc", "name"}, set(), True, requests)
    assert not errors and sum(o["action"] == "inherit_static" for o in shared_overlays) == 1, errors
    print("OK  rebuild_with_vanilla.py: 嵌套root/跨人物/project→promote静态继承自检通过")


def test_explicit_insert_and_duplicate_guard() -> None:
    import rebuild_with_vanilla as rebuild
    from rebuild_with_vanilla import build_expected

    donor = """country_event = {
 id = podt.9
 option = {
  add_country_leader_role = {
   character = RNC_nehru
   country_leader = {
    desc = CBIO_nehru_desc
    ideology = liberalism
   }
  }
 }
}
"""
    vanilla = """country_event = {
 id = podt.9
 option = {
  name = podt.9.a
 }
}
country_event = {
 id = podt.12
 option = {
  add_country_leader_role = {
   character = RNC_nehru
   country_leader = {
    ideology = liberalism
   }
  }
 }
}
"""
    line = next(index for index, text in enumerate(donor.splitlines(), 1) if "desc = CBIO_nehru_desc" in text)
    spec = ("podt.txt", line, "CBIO_nehru_desc")
    approved = {spec: {"container": "country_leader", "root": "podt.12", "character": "RNC_nehru", "ideology": "liberalism"}}
    original = rebuild.APPROVED_EXPLICIT_INSERTS
    try:
        rebuild.APPROVED_EXPLICIT_INSERTS = approved
        expected, overlays, errors = build_expected("podt.txt", donor, vanilla, {"desc"}, {"CBIO_nehru_desc"}, False, [])
        assert not errors, errors
        assert expected is not None and expected.count("desc = CBIO_nehru_desc") == 1, expected
        assert "id = podt.12" in expected
        overlay = next(o for o in overlays if o.get("explicit_approval"))
        assert overlay["root"] == "podt.12" and overlay["action"] == "insert" and overlay["person_id"] == "RNC_nehru", overlay
        old_start = expected.index("id = podt.9")
        old_end = expected.index("id = podt.12")
        assert "CBIO_nehru_desc" not in expected[old_start:old_end], "旧事件不得写入"

        for bad in (
            {spec: dict(approved[spec], root="podt.9")},
            {spec: dict(approved[spec], character="RNC_other")},
        ):
            rebuild.APPROVED_EXPLICIT_INSERTS = bad
            _, _, bad_errors = build_expected("podt.txt", donor, vanilla, {"desc"}, {"CBIO_nehru_desc"}, False, [])
            assert bad_errors, "显式落点目标不唯一或身份不符必须失败"

        shared_donor = """characters = {
 RNC_nehru = {
  instance = {
   country_leader = {
    desc = CBIO_nehru_desc
    ideology = liberalism
   }
  }
 }
}
"""
        shared_vanilla = shared_donor.replace("    desc = CBIO_nehru_desc\n", "")
        requests = [{"person_id": "RNC_nehru", "value": "CBIO_nehru_desc"}]
        shared_expected, shared_overlays, errors = build_expected("shared.txt", shared_donor, shared_vanilla, {"desc", "name"}, set(), True, requests)
        assert not errors, errors
        assert shared_expected is not None and shared_expected.count("desc = CBIO_nehru_desc") == 1, shared_expected
        assert [o["action"] for o in shared_overlays if o.get("static_character")] == ["inherit_static"], shared_overlays
    finally:
        rebuild.APPROVED_EXPLICIT_INSERTS = original
    print("OK  rebuild_with_vanilla.py: 显式裁定落点/旧事件不写入/静态重复拦截自检通过")


CASES = [
    ("check_encoding.py", fault_strip_bom, None, None),
    ("check_localisation.py", fault_duplicate_key, None, None),
    ("check_aliases.py", fault_alias_missing_target, None, None),
    ("check_text_quality.py", fault_text_residue, None, None),
    ("check_human_decisions.py", fault_delete_protected, None, None),
    ("check_human_decisions.py", fault_ledger_parity, None, None),
    ("check_human_decisions.py", fault_ledger_reverse_parity, None, None),
    ("check_human_decisions.py", fault_ledger_marker_missing, None, None),
    ("check_snapshot.py", fault_snapshot_version, None, None),
    ("check_script_structure.py", fault_unbalanced_brace, None, None),
    ("check_desc_semantics.py", fault_desc_wrong_level, None, None),
    ("check_diff_whitelist.py", fault_forbidden_diff, setup_git_fixture, None),
    ("check_diff_whitelist.py", fault_unused_exact_exception, setup_git_fixture, None),
    ("compare_with_vanilla.py", fault_vanilla_semantics, setup_vanilla_fixture, None),
    ("verify_build.py", fault_zip_tamper, setup_build_fixture, build_version_args),
    ("verify_build.py", fault_zip_duplicate, setup_build_fixture, build_version_args),
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

try:
    test_rebuild_overlay()
    test_rebuild_whitespace()
    test_rebuild_restore()
    test_verify_build_semantics()
    test_character_identity()
    test_explicit_insert_and_duplicate_guard()
except Exception as exc:
    failures.append(f"rebuild_with_vanilla.py: {type(exc).__name__}: {exc}")

print(f"\nself_test: cases={len(CASES) + 6} failures={len(failures)}")
for f in failures:
    print("FAIL", f)
raise SystemExit(1 if failures else 0)
