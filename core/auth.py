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
