"""Config file loading for sim-scenario-drafter.

The config is optional TOML. It contains connection details only — never API
keys. For hosted OpenAI-compatible endpoints that require a key, point
``api_key_env`` at the NAME of an environment variable; the secret value
itself must never be written to disk.

Default search order:
1. --config argument
2. ./simscenario.toml
3. ~/.config/simscenario/config.toml
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TIMEOUT = 120


@dataclass(frozen=True)
class EndpointConfig:
    base_url: str = ""
    model: str = ""
    api_key_env: str = ""
    timeout_seconds: int = DEFAULT_TIMEOUT
    path: str = ""

    @property
    def is_configured(self) -> bool:
        return bool(self.base_url and self.model)

    def secret(self) -> str:
        """Look up the API key from the configured env var NAME, if any.
        The value never lives in a file."""
        if not self.api_key_env:
            return os.environ.get("OPENAI_API_KEY", "")
        return os.environ.get(self.api_key_env, "")

    def masked(self) -> str:
        if not self.is_configured:
            return "not configured"
        key_hint = "key via env" if self.secret() else "no key (fine for Ollama)"
        return f"{self.base_url} model={self.model} ({key_hint})"


DEFAULT_CONFIG_FILES = ("simscenario.toml", "simscenario.toml.example")


def default_config_path() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(xdg) / "simscenario" / "config.toml"


def _coerce_timeout(value, default=DEFAULT_TIMEOUT):
    try:
        n = int(float(value))
        return n if n > 0 else default
    except (TypeError, ValueError):
        return default


def _parse_toml(text):
    """Minimal TOML parsing stdlib-first (tomllib on 3.11+, naive fallback)."""
    try:
        import tomllib
        return tomllib.loads(text)
    except ModuleNotFoundError:
        pass
    # Very small TOML subset: [section] headers + key = value strings/numbers.
    data = {}
    section = None
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line:
            continue
        if line.startswith("["):
            section = line.strip("[]").strip().split(".")[-1]
            data.setdefault(section, {})
        elif "=" in line and section is not None:
            k, _, v = line.partition("=")
            v = v.strip().strip('"').strip("'")
            data[section][k.strip()] = v
    return data


def load_config(path=None) -> EndpointConfig:
    """Load endpoint config from an optional TOML file. Missing file is fine:
    the tool simply runs in offline template mode."""
    candidates = [Path(path)] if path else [
        Path(DEFAULT_CONFIG_FILES[0]),
        default_config_path(),
    ]
    for candidate in candidates:
        if not candidate.is_file():
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
            data = _parse_toml(text)
        except (OSError, ValueError) as exc:
            print(f"warning: could not parse {candidate}: {exc}", file=sys.stderr)
            return EndpointConfig(path=str(candidate))
        endpoint = data.get("endpoint", {}) if isinstance(data, dict) else {}
        return EndpointConfig(
            base_url=str(endpoint.get("base_url", "")).rstrip("/"),
            model=str(endpoint.get("model", "")),
            api_key_env=str(endpoint.get("api_key_env", "")),
            timeout_seconds=_coerce_timeout(endpoint.get("timeout_seconds")),
            path=str(candidate),
        )
    return EndpointConfig(path="") if path else EndpointConfig()
