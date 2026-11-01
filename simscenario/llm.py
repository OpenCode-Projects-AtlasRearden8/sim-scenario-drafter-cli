"""OpenAI-compatible chat client (works with Ollama, llama.cpp server,
LM Studio, vLLM, OpenAI itself, and anything speaking the same wire format).

No API keys are stored anywhere: if an endpoint needs one, the config names
an environment variable and the key is read from the environment at call time.

All failures raise LLMError so callers can fall back to offline templates.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

SYSTEM_PROMPT = (
    "You are a nursing simulation education assistant. You draft fictional practice "
    "scenarios for training only. You never give medical advice and you never imply "
    "your output applies to real patients. Reply with a single JSON object, no prose, "
    "no code fences."
)


class LLMError(RuntimeError):
    pass


def build_user_prompt(skill_id, room_id, meta_skill, meta_room):
    return (
        f"Draft a fictional nursing simulation practice scenario packet.\n"
        f"Skill: {skill_id} ({meta_skill.get('title', '')}).\n"
        f"Room: {room_id} ({meta_room.get('title', '')}).\n"
        "Return JSON with keys: skill_id, room_id, skill_title, room_title, "
        "objectives (5 items), room_setup (2-4 sentences), ambient_noise (one line), "
        "patient_statements (at least 6 realistic first-person lines a role-player says, "
        "ordered: opening, mid-scenario, closing), distractions (3 items), "
        "props (5-10 items), expected_actions (5 items), debrief_questions (5 items). "
        "Everything is fictional and for adult learners practicing skills. "
        "No real patient data, no real medication protocols."
    )


def chat_completion(base_url, model, user_prompt, api_key="", timeout=120,
                    temperature=0.7):
    """POST /chat/completions to an OpenAI-compatible server and return the
    assistant message content as a string."""
    if not base_url or not model:
        raise LLMError("base_url and model are required")
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "stream": False,
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise LLMError(f"endpoint returned HTTP {exc.code}") from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise LLMError(f"could not reach endpoint: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise LLMError(f"endpoint returned non-JSON body: {exc}") from exc

    try:
        content = body["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise LLMError("endpoint returned an empty message content")
        return content
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(f"unexpected response shape: {exc}") from exc


def parse_json_payload(content):
    """Extract and parse the first JSON object from a model reply. Tolerates
    code fences and surrounding prose."""
    text = content.strip()
    if text.startswith("```"):
        # Drop ```json style fences.
        first_line_end = text.find("\n")
        text = text[first_line_end + 1:] if first_line_end != -1 else text.strip("`")
        end = text.rfind("```")
        if end != -1:
            text = text[:end]
        text = text.strip()
    # Try to slice out a balanced {...} object if prose surrounds it.
    start = text.find("{")
    if start > 0 or (start == 0 and not text.rstrip().endswith("}")):
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMError(f"could not parse JSON from model reply: {exc}") from exc


def draft_via_llm(cfg, skill_id, room_id, meta_skill, meta_room):
    """Try an LLM draft; return the raw payload dict or raise LLMError."""
    content = chat_completion(
        base_url=cfg.base_url,
        model=cfg.model,
        user_prompt=build_user_prompt(skill_id, room_id, meta_skill, meta_room),
        api_key=cfg.secret(),
        timeout=cfg.timeout_seconds,
    )
    payload = parse_json_payload(content)
    if not isinstance(payload, dict):
        raise LLMError("model reply JSON is not an object")
    return payload
