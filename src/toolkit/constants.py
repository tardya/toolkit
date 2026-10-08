import json

from pathlib import Path

CONF_PATH = Path("config.json")

def load_cfg(path: Path) -> dict:
    """загружает файл конфигурации с коэффицентами"""
    if not path.exists():
        return {"length": {}, "mass": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

CFG = load_cfg(CONF_PATH)