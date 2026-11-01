"""CLI: simscenario — draft for-practice nursing simulation scenario packets."""

from __future__ import annotations

import argparse
import sys

from . import DEFAULT_FALLBACK_HINT, __version__
from . import data
from .config import load_config
from .drafter import SOURCE_FALLBACK, SOURCE_LLM, batch_packets, draft_packet
from .packet import PacketError, export_batch, export_markdown, render_markdown

BANNER = f"sim-scenario-drafter v{__version__} — education-only simulation drafting"


def _print_packet(markdown_text, notes, source, out_path=None):
    print(markdown_text, end="" if markdown_text.endswith("\n") else "\n")
    for note in notes or []:
        if note:
            print(f"note: {note}", file=sys.stderr)
    dest = f" -> {out_path}" if out_path else ""
    print(f"[artifact label: for-practice · education only · never medical advice] "
          f"[source: {source}]{dest}", file=sys.stderr)


def _check_ids(skill, room):
    bad = []
    if skill and skill not in data.SKILLS:
        bad.append("skill")
    if room and room not in data.ROOMS:
        bad.append("room")
    return bad


def _nearest(kind, supplied):
    """Suggest closest known id for a nicer error message."""
    import difflib
    table = data.SKILLS if kind == "skill" else data.ROOMS
    match = difflib.get_close_matches(supplied, table.keys(), n=1)
    return match[0] if match else None


def cmd_draft(args, cfg):
    bad = _check_ids(args.skill, args.room)
    if bad:
        kind, val = bad[0], args.skill if bad[0] == "skill" else args.room
        near = _nearest(kind, val)
        hint = f" (closest: {near})" if near else ""
        print(f"error: unknown {kind} id {val!r}{hint}. "
              f"Run 'simscenario {'skills' if kind == 'skill' else 'rooms'}' "
              "to list valid ids.", file=sys.stderr)
        return 2
    notes = []
    packet = draft_packet(cfg, args.skill, args.room,
                          force_fallback=args.offline,
                          attempt_report=notes)
    source = packet.get("source", SOURCE_FALLBACK)
    md = render_markdown(packet, footer=DEFAULT_FALLBACK_HINT)
    out_path = None
    if args.out:
        out_path = export_markdown(packet, args.out)
    _print_packet(md, [n for _, n in notes if n], source, out_path)
    return 0


def cmd_batch(args, cfg):
    skills = [s.strip() for s in args.skills.split(",") if s.strip()] if args.skills else None
    rooms = [r.strip() for r in args.rooms.split(",") if r.strip()] if args.rooms else None
    for kind, values in (("skill", skills), ("room", rooms)):
        table = data.SKILLS if kind == "skill" else data.ROOMS
        for val in values or []:
            if val not in table:
                near = _nearest(kind, val)
                hint = f" (closest: {near})" if near else ""
                print(f"error: unknown {kind} id {val!r}{hint}", file=sys.stderr)
                return 2
    packets, reports = batch_packets(
        args.count, cfg, skills=skills, rooms=rooms, force_fallback=args.offline,
    )
    written = export_batch(packets, args.out, prefix=args.prefix)
    llm_used = sum(1 for p in packets if p.get("source") == SOURCE_LLM)
    for (skill, room), notes in reports:
        note = notes[0][1] if notes else None
        if note:
            print(f"note [{skill}/{room}]: {note}", file=sys.stderr)
    print(f"exported {len(written)} for-practice packets to {args.out} "
          f"({llm_used} via LLM, {len(written) - llm_used} via offline template fallback)",
          file=sys.stderr)
    print(f"all artifacts labeled for-practice · education only · never medical advice",
          file=sys.stderr)
    return 0


def cmd_list(kind):
    table = data.SKILLS if kind == "skills" else data.ROOMS
    if args := table.values():
        print(f"available {kind} (education-only simulation content):")
        for entry in table.values():
            print(f"  {entry['id']:<32} {entry['title']}")
        print("\nUse ids with: simscenario draft --skill <id> --room <id>")
    return 0


def cmd_config_example():
    print("""\
# simscenario.toml — optional config. No API keys go in this file.
# Works with any OpenAI-compatible endpoint, including local Ollama.
[endpoint]
base_url = "http://localhost:11434/v1"   # Ollama's OpenAI-compatible base
model = "llama3.1:8b"                    # any model you have pulled
# For hosted endpoints only: exact NAME of the env var holding the key.
# (Ollama needs none.) The key value itself must never be written to disk.
api_key_env = ""
timeout_seconds = 120

# Save as simscenario.toml next to where you run the command, or set its
# path with --config. Without a config, drafts use the offline template
# fallback, so the tool always works.""")


def build_parser():
    p = argparse.ArgumentParser(
        prog="simscenario",
        description=(
            "Education-only CLI that drafts nursing simulation practice "
            "scenario packets (patient statements, planned distractions, prop "
            "list, debrief questions). Training material — never medical advice."
        ),
        epilog=(
            "Every generated artifact is labeled for-practice. Education use only."
        ),
    )
    p.add_argument("--version", action="version", version=f"simscenario {__version__}")
    p.add_argument("--config", help="path to an optional simscenario.toml")
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("draft", help="draft one scenario packet")
    d.add_argument("--skill", help=f"skill id (see 'simscenario skills'); default: {next(iter(data.SKILLS))}")
    d.add_argument("--room", help=f"room id (see 'simscenario rooms'); default: {next(iter(data.ROOMS))}")
    d.add_argument("--out", help="also write the packet to this directory as Markdown")
    d.add_argument("--offline", action="store_true",
                   help="skip the LLM and force the offline template fallback")
    d.set_defaults(func=cmd_draft)

    b = sub.add_parser("batch", help="draft and export a batch of scenario packets")
    b.add_argument("--count", type=int, default=6, help="number of packets (default 6)")
    b.add_argument("--out", default="simscenario_batches", help="output directory")
    b.add_argument("--skills", help="comma-separated skill ids to cycle through")
    b.add_argument("--rooms", help="comma-separated room ids to cycle through")
    b.add_argument("--prefix", default="scenario", help="filename prefix")
    b.add_argument("--offline", action="store_true", help="force offline template fallback")
    b.set_defaults(func=cmd_batch)

    s = sub.add_parser("skills", help="list available skills")
    s.set_defaults(func=lambda a, c: cmd_list("skills"))

    r = sub.add_parser("rooms", help="list available rooms")
    r.set_defaults(func=lambda a, c: cmd_list("rooms"))

    ce = sub.add_parser("config-example", help="print a sample config file (no keys)")
    ce.set_defaults(func=lambda a, c: (cmd_config_example(), 0)[1])

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    cfg = load_config(getattr(args, "config", None))
    try:
        return args.func(args, cfg)
    except PacketError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
