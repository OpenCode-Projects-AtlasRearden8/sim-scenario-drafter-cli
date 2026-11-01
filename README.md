# sim-scenario-drafter

**Education-only CLI that drafts nursing simulation practice scenario packets.**
Training material for skills labs and role-play — **never medical advice**.

Pick a skill and a realistic room, and the tool drafts a printable Markdown
packet containing:

- **Patient statements** — realistic first-person lines for a trained
  role-player, organized into Opening / Mid-scenario / Closing phases
- **Planned distractions** — deliberate, scripted interruptions to make the
  scenario real
- **Prop list** — simulation props only, merged from the skill and the room
- **Debrief questions** — plus learning objectives, room setup, ambient noise
  cues, and an expected-actions checklist for the facilitator

Every artifact carries a **for-practice** label and a clear
*education-only · never medical advice* disclaimer, top and bottom.

## Who it's for

Nurse educators, simulation-lab coordinators, preceptors, students forming
practice groups, and anyone building training days on a budget — including
everything published by **Asdale Dynamics, LLC**. Built in plain English and
runs fully local-first.

## Install

Requires Python 3.9+. No third-party runtime dependencies.

```bash
pip install .
```

Or run straight from a checkout:

```bash
python -m simscenario --help
```

## Quick start

```bash
simscenario skills                 # list skills
simscenario rooms                  # list rooms

# Works immediately, fully offline, from the built-in template library:
simscenario draft --skill hand-hygiene --room med-surg-double

# Also save to a directory as Markdown:
simscenario draft --skill fall-risk --room home-health-bedroom --out packets/

# Draft and export a batch of packets (prints progress and labels):
simscenario batch --count 6 --out batch/

# Print a sample config file (contains no keys):
simscenario config-example
```

## Using a local LLM (Ollama) or any OpenAI-compatible endpoint

The draft upgrade path is optional. Save a small TOML file named
`simscenario.toml` next to where you run the command (or pass `--config`):

```toml
[endpoint]
base_url = "http://localhost:11434/v1"   # Ollama's OpenAI-compatible base
model = "llama3.1:8b"                    # any model you have pulled
api_key_env = ""                         # none needed for Ollama
timeout_seconds = 120
```

`simscenario draft` will now try the endpoint first — Ollama, LM Studio,
llama.cpp server, vLLM, OpenAI, anything speaking the OpenAI wire format —
and **fall back to the offline template library whenever the endpoint is
down, slow, or returns unusable output**. Your drafts never fail.

Many teams prefer staying fully offline, which is the default with no config.

## Keys and privacy — house rules

- **No API keys ever go in files.** For hosted endpoints, set `api_key_env`
  to the *name* of an environment variable; the key is read from the
  environment at call time. For Ollama, leave it empty.
- Nothing is sent anywhere except the endpoint you configure. No config is
  the same as airplane mode.

## Education-only guardrails

- All patients, statements, medications, and orders are fictional.
- The renderer refuses to output an artifact that lacks the practice label
  (`ensure_labeled` guard in `simscenario/packet.py`).
- Renders the same content whether drafted by an LLM or the offline
  templates, so quality review stays meaningful.

Batch exports write one Markdown file per scenario, numbered and labeled:
`batch/scenario_001_hand-hygiene_med-surg-double.md`.

## Commands

| Command | Purpose |
| --- | --- |
| `skills` | list available skills |
| `rooms` | list available rooms |
| `draft` | draft one packet (`--skill`, `--room`, `--out`, `--offline`) |
| `batch` | draft and export many packets (`--count`, `--out`, `--skills`, `--rooms`, `--prefix`, `--offline`) |
| `config-example` | print a no-keys sample config |

## Tests

```bash
pip install .[dev]
pytest
```

The suite (35 tests) mocks all HTTP responses — no network is touched.

## How this is different

Complements, but is distinct from, our related tools:

- **nclex-style-quiz-trainer** — quizzes knowledge; this drafts full scenario
  packets for live role-play.
- **sbar-report-builder-webapp** — builds SBAR handoffs; this builds the
  simulation itself (script, distractions, props, debrief).
- **shift-brain-sheet-maker** — organizes a nurse's working shift; this plans
  practice encounters in a lab room.

## Credits and license

Built for beginners and educators alike by **Asdale Dynamics, LLC**.
Dylan Asdale — RN turned AI author — explains AI plainly at
[dylanasdale.github.io](https://dylanasdale.github.io) and in the book
*The Massive AI Manual*.

MIT licensed. See `LICENSE` (Copyright (c) 2026 Asdale Dynamics, LLC).
Education only. Never medical advice.
