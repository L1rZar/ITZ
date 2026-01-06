# -*- coding: utf-8 -*-
"""
Система сохранений через JSON, привязанная к логину.
Файл на игрока: data/players/<login>.json
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
PLAYERS_DIR = os.path.join(DATA_DIR, "players")


def _ensure_dirs():
    """Просто создать папку для сохранений, если её ещё нет."""
    if not os.path.exists(PLAYERS_DIR):
        os.makedirs(PLAYERS_DIR)


def save_state(state: dict):
    """Записать текущее состояние игрока в JSON."""
    _ensure_dirs()
    login = state.get("login")
    if not login:
        return
    path = os.path.join(PLAYERS_DIR, f"{login}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_state(login: str):
    """Прочитать состояние игрока из JSON. Если файла нет — вернуть None."""
    _ensure_dirs()
    path = os.path.join(PLAYERS_DIR, f"{login}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_new_state(login: str) -> dict:
    """
    Создать минимальное начальное состояние.
    Герой выбирается позже в интро.
    """
    _ensure_dirs()
    state = {
        "login": login,
        "chapter": 0,
        "artifacts": [],
        "inventory": {"medkit": 1},
        "clarity_points": 0,
        "flags": {},
    }
    save_state(state)
    return state
