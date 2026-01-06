import json
import os

ACCOUNTS = "data/accounts.txt"


def register_or_login(new=False):
    """Регистрация или вход."""
    # Создаём файл если нет
    os.makedirs(os.path.dirname(ACCOUNTS), exist_ok=True)
    if not os.path.exists(ACCOUNTS):
        with open(ACCOUNTS, 'w', encoding='utf-8') as f:
            f.write('tester:password\n')

    login = input('Логин: ').strip()
    pwd = input('Пароль: ').strip()

    # Читаем всех пользователей
    users = {}
    try:
        with open(ACCOUNTS, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    u, p = line.strip().split(':', 1)
                    users[u] = p
    except FileNotFoundError:
        pass  # файл пустой

    if new:
        if login in users:
            print('Пользователь уже существует.')
            return None
        # Добавляем нового
        with open(ACCOUNTS, 'a', encoding='utf-8') as f:
            f.write(f"{login}:{pwd}\n")
        print('Аккаунт создан.')
        return login
    else:
        if users.get(login) == pwd:
            print('Успешный вход.')
            return login
        print('Пароль неверен.')
        return None

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
