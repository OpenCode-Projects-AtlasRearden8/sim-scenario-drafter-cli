"""Config loading tests."""

import os
from pathlib import Path

import pytest

from simscenario.config import EndpointConfig, default_config_path, load_config


def test_default_when_no_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    Path(default_config_path()).parent.mkdir(parents=True, exist_ok=True)
    cfg = load_config()
    assert not cfg.is_configured
    assert cfg.secret() == ""


def test_load_ollama_style_config(tmp_path, monkeypatch):
    path = tmp_path / "simscenario.toml"
    path.write_text(
        '[endpoint]\n'
        'base_url = "http://localhost:11434/v1"\n'
        'model = "llama3.1:8b"\n'
        'api_key_env = ""\n'
        'timeout_seconds = 60\n',
        encoding="utf-8",
    )
    cfg = load_config(path)
    assert cfg.is_configured
    assert cfg.base_url == "http://localhost:11434/v1"
    assert cfg.model == "llama3.1:8b"
    assert cfg.timeout_seconds == 60


def test_no_key_ever_stored_on_disk(tmp_path, monkeypatch):
    path = tmp_path / "simscenario.toml"
    path.write_text('[endpoint]\nbase_url = "https://api.example.com/v1"\nmodel = "x"\n'
                    'api_key_env = "MY_TEST_KEY_ENV"\n', encoding="utf-8")
    monkeypatch.delenv("MY_TEST_KEY_ENV", raising=False)
    cfg = load_config(path)
    assert cfg.secret() == ""
    monkeypatch.setenv("MY_TEST_KEY_ENV", "sk-abc123")
    assert cfg.secret() == "sk-abc123"
    # The key value never appears in the config file contents.
    assert "sk-abc123" not in path.read_text(encoding="utf-8")


def test_falls_back_to_openai_api_key_env(tmp_path):
    cfg = EndpointConfig(base_url="https://api.example.com/v1", model="m")
    monkeypatch_env = {"OPENAI_API_KEY": "sk-env"}
    for k, v in monkeypatch_env.items():
        os.environ[k] = v
    try:
        assert cfg.secret() == "sk-env"
    finally:
        del os.environ["OPENAI_API_KEY"]


def test_bad_timeout_is_coerced(tmp_path):
    path = tmp_path / "c.toml"
    path.write_text('[endpoint]\nbase_url = "http://x/v1"\nmodel = "m"\n'
                    'timeout_seconds = "not a number"\n', encoding="utf-8")
    assert load_config(path).timeout_seconds == 120
