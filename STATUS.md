# STATUS — sim-scenario-drafter-cli

Last updated: 2026-11-01

## What was built

`sim-scenario-drafter` — an education-only CLI that drafts **nursing
simulation practice scenario packets** as printable Markdown. Training
material for skills labs and role-play; **never medical advice**; every
artifact is labeled `for-practice`.

- **9 skills** (hand hygiene, vital signs, IV start, simulated oral med pass,
  wound care, oxygen therapy, fall risk, discharge teaching, pressure injury
  prevention), each with objectives, realistic patient statements, planned
  distractions, prop lists, expected learner actions, and debrief questions.
- **6 rooms** (med-surg double, ambulatory exam, long-term care, home health
  bedroom, pre-op holding, skills lab) providing setup description, ambient
  noise cues, and room-specific props.
- **Drafting pipeline:** optional OpenAI-compatible endpoint (Ollama, LM
  Studio, vLLM, etc.) via a TOML config file with no keys in files — then a
  **full offline template fallback** so drafts never fail. Batch export
  numbers and dedups files automatically.
- **Safety guardrails:** `ensure_labeled()` refuses to export any artifact
  that lacks the practice label; no keys on disk; no telemetry; stdlib-only
  runtime (urllib).

## How to run

```bash
pip install .                          # or: python -m simscenario from a checkout
simscenario skills / rooms             # list ids
simscenario draft --skill hand-hygiene --room med-surg-double --out packets/
simscenario batch --count 6 --out batch/
simscenario config-example             # print a no-keys sample config
python -m pytest                       # 35 tests, all mocked, no network
```

Config (`simscenario.toml` next to the working directory, or `--config`):

```toml
[endpoint]
base_url = "http://localhost:11434/v1"  # Ollama's OpenAI-compatible base
model = "llama3.1:8b"
api_key_env = ""                        # empty for Ollama; NAME of env var for hosted
timeout_seconds = 120
```

## Verification results (this workspace)

- `pytest`: **35 passed, 0 failed** — system Python 3.13 and a clean venv.
- CLI smoke tests: `--version`, `skills`, `rooms`, `config-example`,
  offline `draft` with file export, unknown-id errors with closest-match
  hints, offline `batch` 4/9/12 — all passed.
- Real end-to-end HTTP check against a local mock OpenAI-compatible server
  (fenced-JSON reply): `draft` and `batch` both exercised the LLM path
  (`source: llm`), and unreachability gracefully fell back offline.
- All exported batch packets (12/12) verified to contain the FOR PRACTICE
  banner; `grep -L` found zero unlabeled artifacts.
- Console script `simscenario` from `pip install -e .` verified in a fresh
  venv (stdlib-only runtime; only pytest needed for dev).

## Known gaps / next steps

- No `--explain`/doctor command yet for troubleshooting endpoint configs.
- Ollama tested via its OpenAI-compatible wire format against a mock
  server; a live-model pull wasn't possible in this environment, so first
  run against a real Ollama may reveal prompt-tuning wants.
- No DOCX/PDF export (Markdown prints fine; more formats can follow).
- Skills/rooms catalogues are curated, not configurable via user YAML yet.
- No fuzzy-match stylesheet for custom skill/room definition imports.
