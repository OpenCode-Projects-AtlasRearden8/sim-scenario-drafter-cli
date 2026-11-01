"""Packet build/render/export tests."""

import pytest

from simscenario import PRACTICE_BANNER, __version__
from simscenario.cli import main as cli_main
from simscenario.packet import (
    PacketError,
    build_packet,
    ensure_labeled,
    export_batch,
    export_markdown,
    render_markdown,
)


def test_build_packet_from_fallback():
    p = build_packet("hand-hygiene", "med-surg-double")
    assert p["skill_id"] == "hand-hygiene"
    assert p["room_id"] == "med-surg-double"
    assert set(p["patient_statements"]) >= {"Opening", "Mid-scenario", "Closing"}
    assert all(len(v) >= 1 for v in p["patient_statements"].values())
    assert len(p["props"]) >= 3
    assert len(p["debrief_questions"]) >= 3


def test_build_packet_fuzzy_id_normalization():
    p = build_packet("Hand Hygiene", "med surg double")
    assert p["skill_id"] == "hand-hygiene"
    assert p["room_id"] == "med-surg-double"


def test_build_packet_rejects_unknown():
    with pytest.raises(PacketError):
        build_packet("nope", "med-surg-double")
    with pytest.raises(PacketError):
        build_packet("hand-hygiene", "narnia")


def test_build_packet_merges_llm_props_without_duplicates():
    llm_payload = {"props": ["Alcohol-based hand rub dispensers at door and bedside", "extra prop"]}
    p = build_packet("hand-hygiene", "skills-lab", payload=llm_payload)
    assert "extra prop" in p["props"]
    assert len(p["props"]) == len(set(p["props"]))


def test_build_packet_repairs_short_llm_statements():
    llm_payload = {"patient_statements": ["only one line"]}
    p = build_packet("hand-hygiene", "med-surg-double", payload=llm_payload)
    all_stmts = [s for v in p["patient_statements"].values() for s in v]
    assert len(all_stmts) >= 3


def test_build_packet_rejects_invalid_llm_types():
    with pytest.raises(PacketError):
        build_packet("hand-hygiene", "med-surg-double", payload={"props": "one string"})


def test_render_markdown_labels_every_section():
    p = build_packet("wound-care", "home-health-bedroom")
    md = render_markdown(p)
    assert PRACTICE_BANNER in md
    assert md.count("for-practice") >= 1 or md.count("FOR PRACTICE") >= 1
    assert "not medical advice" in md.lower()
    assert "## Prop list" in md
    assert "## Debrief questions" in md
    assert "“" in md  # patient statements are quoted
    assert "wound" in md.lower()


def test_render_rejects_invalid_packet():
    with pytest.raises(PacketError):
        render_markdown({"nope": True})


def test_ensure_labeled_guard():
    ensure_labeled(PRACTICE_BANNER + " text")
    with pytest.raises(PacketError):
        ensure_labeled("completely unlabeled generic text")


def test_export_writes_file_with_label(tmp_path):
    p = build_packet("vital-signs", "ambulatory-exam")
    path = export_markdown(p, tmp_path)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert PRACTICE_BANNER in text
    assert f"sim-scenario-drafter v{__version__}" in text


def test_export_batch_numbered_and_printable(tmp_path):
    pairs = [("hand-hygiene", "med-surg-double"), ("vital-signs", "skills-lab")]
    packets = [build_packet(s, r) for s, r in pairs] * 3
    written = export_batch(packets, tmp_path, prefix="demo")
    assert len(written) == 6
    names = sorted(w.name for w in written)
    assert names[0].startswith("demo_001_")
    assert all(n.endswith(".md") for n in names)
    assert all(path.read_text(encoding="utf-8").startswith("# Simulation")
               for path in written)


def test_cli_skills_and_rooms_lists(capsys):
    assert cli_main(["skills"]) == 0
    out = capsys.readouterr().out
    assert "hand-hygiene" in out
    assert cli_main(["rooms"]) == 0
    out = capsys.readouterr().out
    assert "med-surg-double" in out


def test_cli_draft_offline_prints_packet(capsys, tmp_path):
    rc = cli_main(["draft", "--skill", "fall-risk", "--room", "long-term-care",
                   "--offline", "--out", str(tmp_path)])
    assert rc == 0
    err = capsys.readouterr().err
    assert "for-practice" in err
    md_files = list(tmp_path.glob("*.md"))
    assert len(md_files) == 1
    assert PRACTICE_BANNER in md_files[0].read_text(encoding="utf-8")


def test_cli_draft_unknown_skill_lists_closest(capsys):
    rc = cli_main(["draft", "--skill", "hand-hygin"])
    assert rc == 2
    assert "closest: hand-hygiene" in capsys.readouterr().err


def test_cli_batch_offline(capsys, tmp_path):
    rc = cli_main(["batch", "--count", "4", "--out", str(tmp_path),
                   "--skills", "hand-hygiene,fall-risk", "--offline"])
    assert rc == 0
    files = sorted(p.name for p in tmp_path.glob("*.md"))
    assert len(files) == 4
    err = capsys.readouterr().err
    assert "offline template fallback" in err


def test_cli_batch_unknown_room_fails_cleanly(capsys, tmp_path):
    rc = cli_main(["batch", "--count", "2", "--out", str(tmp_path), "--rooms", "bogus-room"])
    assert rc == 2


def test_cli_config_example_has_no_key(capsys):
    assert cli_main(["config-example"]) == 0
    out = capsys.readouterr().out
    assert "api_key_env" in out
    assert "sk-" not in out
