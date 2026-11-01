"""Draft orchestration: LLM first (if configured), offline template fallback second."""

from __future__ import annotations

from . import data, llm
from .config import EndpointConfig
from .packet import build_packet

SOURCE_LLM = "llm"
SOURCE_FALLBACK = "offline-template-fallback"


def draft_packet(config=EndpointConfig(), skill_id=None, room_id=None,
                 force_fallback=False, attempt_report=None):
    """Return a packet dict for skill_id + room_id.

    Priority: configured OpenAI-compatible/Ollama endpoint -> offline template
    fallback. If attempt_report is a list, a (source, error) note is appended
    describing which path produced the packet.
    """
    skill_id = skill_id or next(iter(data.SKILLS))
    room_id = room_id or next(iter(data.ROOMS))
    if skill_id not in data.SKILLS or room_id not in data.ROOMS:
        # build_packet validates ids and raises PacketError.
        return build_packet(skill_id, room_id, source=SOURCE_FALLBACK)

    notes = []
    if not force_fallback and config.is_configured:
        try:
            payload = llm.draft_via_llm(
                config, skill_id, room_id,
                data.SKILLS[skill_id], data.ROOMS[room_id],
            )
            packet = build_packet(skill_id, room_id, payload=payload,
                                  source=SOURCE_LLM)
            if attempt_report is not None:
                attempt_report.append((SOURCE_LLM, None))
            return packet
        except llm.LLMError as exc:
            notes.append(f"LLM draft unavailable ({exc}); using offline template fallback.")
    elif not force_fallback and not config.is_configured:
        notes.append("No endpoint configured; using offline template fallback.")

    packet = build_packet(skill_id, room_id, source=SOURCE_FALLBACK)
    if attempt_report is not None:
        attempt_report.append((SOURCE_FALLBACK, "; ".join(notes) or None))
    return packet


def batch_packets(count, config=EndpointConfig(), skills=None, rooms=None,
                  force_fallback=False):
    """Cycle through skill/room pairings to build `count` distinct packets."""
    skills = [s for s in (skills or list(data.SKILLS)) if s in data.SKILLS]
    rooms = [r for r in (rooms or list(data.ROOMS)) if r in data.ROOMS]
    if not skills:
        skills = list(data.SKILLS)
    if not rooms:
        rooms = list(data.ROOMS)
    pairs = []
    i = 0
    while len(pairs) < count:
        pairs.append((skills[i % len(skills)], rooms[i % len(rooms)]))
        i += 1
    packets = []
    reports = []
    for skill, room in pairs:
        notes = []
        packets.append(draft_packet(config, skill, room,
                                    force_fallback=force_fallback,
                                    attempt_report=notes))
        reports.append(((skill, room), notes))
    return packets, reports
