"""配置加载与校验"""
import json
from pathlib import Path
from urllib.parse import urlparse

CONFIG_FILE = Path("config.json")
_CONFIG: dict = {}


def load_config() -> dict:
    global _CONFIG
    if _CONFIG:
        return _CONFIG

    if not CONFIG_FILE.exists():
        _CONFIG = {"provider": "ollama", "ollama": {
            "url": "http://127.0.0.1:11434/api/generate", "model": "qwen3:8b"}}
        return _CONFIG

    try:
        _CONFIG = json.loads(CONFIG_FILE.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"config.json 格式错误：{e}")

    provider = _CONFIG.get("provider", "")
    if provider == "ollama":
        ollama = _CONFIG.get("ollama", {})
        if not ollama.get("url") or not ollama.get("model"):
            raise RuntimeError("provider=ollama 时，ollama.url 和 ollama.model 不能为空")
        url = urlparse(ollama["url"])
        if url.scheme != "http" or url.hostname not in ("localhost", "127.0.0.1", "::1"):
            _CONFIG = {}
            raise RuntimeError("Ollama 必须使用本机 http://127.0.0.1 或 localhost 地址")
    else:
        _CONFIG = {}
        raise RuntimeError("此版本只使用本地 Ollama，请设置 provider=ollama")

    return _CONFIG


def get_provider() -> str:
    return load_config()["provider"]


def get_ollama_config() -> dict:
    return load_config().get("ollama", {})


def get_srs_config() -> dict:
    """返回间隔复习配置，并为旧版 config.json 提供安全默认值。"""
    srs = load_config().get("srs", {})
    daily_new_limit = srs.get("daily_new_limit", 20)
    if not isinstance(daily_new_limit, int) or isinstance(daily_new_limit, bool):
        raise RuntimeError("srs.daily_new_limit 必须是整数")
    if not 0 <= daily_new_limit <= 100:
        raise RuntimeError("srs.daily_new_limit 必须在 0 到 100 之间")
    return {"daily_new_limit": daily_new_limit}


def get_sync_config() -> dict:
    sync = load_config().get("sync", {})
    interval = sync.get("interval_seconds", 30)
    if type(interval) is not int or not 10 <= interval <= 3600:
        raise RuntimeError("sync.interval_seconds 必须是 10 到 3600 之间的整数")
    return {"interval_seconds": interval,
            "credentials_dir": sync.get("credentials_dir", ".secrets")}
