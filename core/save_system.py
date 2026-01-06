import json
import os

# Пути к папкам
DATA_DIR = "data/players"

def save_state(state):
    """Сохранить состояние игрока."""
    os.makedirs(DATA_DIR, exist_ok=True)  # создаёт папку если нет
    login = state.get("login")
    if login:
        path = f"{DATA_DIR}/{login}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

def load_state(login):
    """Загрузить состояние игрока."""
    path = f"{DATA_DIR}/{login}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def create_new_state(login):
    """Создать новое состояние."""
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
