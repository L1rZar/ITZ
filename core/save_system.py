# -*- coding: utf-8 -*-
"""
Система сохранений через JSON, привязанная к логину.
"""
"""
Schema `state` (основные поля):

- `login`: str — логин игрока (ключ для файла сохранения).
- `chapter`: int — текущая глава/позиция в истории.
- `artifacts`: list[dict] — список полученных артефактов (каждый — словарь с полем `id`, `name`, `type`, ...).
- `inventory`: dict — простой словарь предметов/количества, например `{"medkit": 1}`.
- `clarity_points`: int — ресурс/очки ясности (игровая механика).
- `flags`: dict — произвольные флаги и триггеры для ветвлений и эффектов.

Пример состояния (JSON):
{
    "login": "tester",
    "chapter": 1,
    "artifacts": [{"id": "perm_hp_20", "name": "Пыль депо", "type": "perm"}],
    "inventory": {"medkit": 1},
    "clarity_points": 0,
    "flags": {"met_old_man": true}
}
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
PLAYERS_DIR = os.path.join(DATA_DIR, 'players')


def ensure_dirs():
    if not os.path.exists(PLAYERS_DIR):
        os.makedirs(PLAYERS_DIR)


def save_state(state: dict):
    ensure_dirs()
    login = state.get('login')
    if not login:
        return
    path = os.path.join(PLAYERS_DIR, f"{login}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_state(login: str):
    ensure_dirs()
    path = os.path.join(PLAYERS_DIR, f"{login}.json")
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_new_state(login: str) -> dict:
    # Создаётся минимальное состояние; герой выбирается в сценах
    ensure_dirs()
    state = {
        'login': login,
        'chapter': 0,
        'artifacts': [],
        'inventory': {'medkit': 1},
        'clarity_points': 0,
        'flags': {}
    }
    save_state(state)
    return state
