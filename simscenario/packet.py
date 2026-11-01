"""Packet building, rendering, and export.

A "packet" is a dict with validated fields. It can come from an LLM
(OpenAI-compatible endpoint) or from the offline template fallback.
Every rendered artifact is labeled FOR PRACTICE.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import DISCLAIMER_FOOTER, PRACTICE_BANNER, __version__
from .data import ROOMS, SKILLS

PHASE_NAMES = ("Opening", "Mid-scenario", "Closing")

_DISCLAIMER_LINE = re.compile(
    r"\b(not medical advice|for practice|for-practice|simulation|training material|fiction)",
    re.IGNORECASE,
)


class PacketError(ValueError):
    pass


def _str_list(value, min_len=1):
    if not isinstance(value, list) or len(value) < min_len:
        raise PacketError("expected a non-empty list")
    out = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise PacketError("expected a non-empty string item")
        out.append(item.strip())
    return out


def build_packet(skill_id, room_id, payload=None, source="fallback-template"):
    """Assemble a validated packet dict from skill/room ids plus optional
    LLM-generated payload fields. Missing or invalid fields are filled from
    the offline template fallback."""
    try:
        # LLM-supplied ids may be aliases; normalise against known catalogues.
        skill_norm = (payload or {}).get("skill_id") or skill_id
        room_norm = (payload or {}).get("room_id") or room_id
        skill = SKILLS.get(_norm(skill_id)) or SKILLS.get(_norm(skill_norm)) \
            or SKILLS.get(skill_id) or SKILLS.get(skill_norm)
        room = ROOMS.get(_norm(room_id)) or ROOMS.get(_norm(room_norm)) \
            or ROOMS.get(room_id) or ROOMS.get(room_norm)
        if skill is None:
            raise PacketError(f"unknown skill: {skill_id!r}")
        if room is None:
            raise PacketError(f"unknown room: {room_id!r}")
        skill_id, room_id = skill["id"], room["id"]

        payload = payload or {}
        stmts = payload.get("patient_statements")
        if stmts is None:
            stmts = skill["patient_statements"]
        stmts = _str_list(stmts)  # short LLM lists get repaired below
        for i, template_stmt in enumerate(skill["patient_statements"] * 2):
            if len(stmts) >= 3:
                break
            stmts.append(f"{template_stmt}")

        phases = {}
        chunk = max(1, len(stmts) // 3)
        for i, name in enumerate(PHASE_NAMES):
            start = i * chunk
            end = start + chunk if i < len(PHASE_NAMES) - 1 else len(stmts)
            phases[name] = stmts[start:end]

        packet = {
            "skill_id": skill_id,
            "skill_title": str(payload.get("skill_title") or skill["title"]),
            "room_id": room_id,
            "room_title": str(payload.get("room_title") or room["title"]),
            "objectives": _str_list(payload.get("objectives") or skill["objectives"], 3),
            "room_setup": str(payload.get("room_setup") or room["description"]),
            "ambient_noise": str(payload.get("ambient_noise") or room["ambient"]),
            "patient_statements": phases,
            "distractions": _str_list(payload.get("distractions") or skill["distractions"], 3),
            "props": _str_list(
                list(dict.fromkeys(
                    list(payload.get("props") or []) + skill["props"] + room["room_props"]
                ))
                if payload.get("props") is not None
                else skill["props"] + room["room_props"],
                3,
            ),
            "expected_actions": _str_list(
                payload.get("expected_actions") or skill["expected_actions"], 3
            ),
            "debrief_questions": _str_list(
                payload.get("debrief_questions") or skill["debrief_questions"], 3
            ),
            "source": str(payload.get("source") or source),
            "packet_version": "1",
        }
        return packet
    except PacketError:
        raise
    except (KeyError, TypeError, AttributeError) as exc:
        raise PacketError(f"invalid packet payload: {exc}") from exc


def _norm(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).strip().lower()).strip("-")


def render_markdown(packet, footer=DISCLAIMER_FOOTER):
    """Render a packet as a printable Markdown artifact, fully labeled
    FOR PRACTICE."""
    try:
        sk = packet["skill_title"]
        rm = packet["room_title"]
        obj = packet["objectives"]
        setup = packet["room_setup"]
        ambient = packet["ambient_noise"]
        phases = packet["patient_statements"]
        distr = packet["distractions"]
        props = packet["props"]
        actions = packet["expected_actions"]
        debrief = packet["debrief_questions"]
        source = packet["source"]
    except (KeyError, TypeError):
        raise PacketError("cannot render an invalid packet")

    lines = [
        f"# Simulation Practice Scenario Packet: {sk}",
        f"### Fictional training setting: {rm}",
        "",
        f"> **{PRACTICE_BANNER}**",
        "",
        "## Learning objectives (fictional simulation goals)",
    ]
    lines += [f"{i}. {o}" for i, o in enumerate(obj, 1)]
    lines += [
        "",
        f"## Room setup: {rm}",
        setup,
        "",
        f"**Ambient noise / drama cues:** {ambient}",
        "",
        "## Prop list (simulation props only, none are real supplies)",
    ]
    lines += [f"- {p}" for p in props]
    lines += ["", "## Scripted patient statements (spoken by a trained role-player)"]
    for phase, stmts in phases.items():
        lines.append(f"### {phase}")
        lines += [f"> “{s}”" for s in stmts]
        lines.append("")
    lines += ["## Planned distractions (deliberate, scripted interruptions)"]
    lines += [f"{i}. {d}" for i, d in enumerate(distr, 1)]
    lines += ["", "## Expected learner actions (checklist for the facilitator)"]
    lines += [f"- [ ] {a}" for a in actions]
    lines += ["", "## Debrief questions (after the simulation)"]
    lines += [f"{i}. {q}" for i, q in enumerate(debrief, 1)]
    lines += [
        "",
        "---",
        f"Generated by sim-scenario-drafter v{__version__} · source: {source}",
        "",
        f"*{footer}*",
        "",
        "**Label: for-practice · education only · never medical advice.**",
    ]
    return "\n".join(lines) + "\n"


def ensure_labeled(text):
    """Guard: refuse to export any artifact that does not carry the practice label."""
    if PRACTICE_BANNER not in text and not _DISCLAIMER_LINE.search(text):
        raise PacketError("artifact lacks a for-practice / education-only label")
    return text


def export_markdown(packet, out_dir, filename=None):
    """Write one packet to out_dir as Markdown. Returns the written path."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    text = ensure_labeled(render_markdown(packet))
    name = filename or f"scenario_{_norm(packet['skill_id'])}_{_norm(packet['room_id'])}.md"
    if not name.endswith((".md", ".markdown")):
        name += ".md"
    path = out_dir / name
    path.write_text(text, encoding="utf-8")
    return path


def export_batch(packets, out_dir, prefix="batch"):
    """Export many packets with numbered, collision-free filenames."""
    written = []
    used = set()
    for i, packet in enumerate(packets, 1):
        base = f"{prefix}_{i:03d}_{_norm(packet['skill_id'])}_{_norm(packet['room_id'])}"
        name, n = base, 0
        while name in used:
            n += 1
            name = f"{base}__{n}"
        used.add(name)
        written.append(export_markdown(packet, out_dir, filename=name))
    return written
