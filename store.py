"""
陪伴玩偶 - JSON 文件存储 (极简单向版)
"""
import json
import os
import time
import threading

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
_lock = threading.Lock()


def _load() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"box_msg": None, "next_id": 1}


def _save(data: dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_box_msg(text: str):
    with _lock:
        data = _load()
        data["box_msg"] = {"id": data["next_id"], "text": text, "ts": time.time()}
        data["next_id"] += 1
        _save(data)


def get_box_msg() -> dict | None:
    return _load().get("box_msg")
