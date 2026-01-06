# -*- coding: utf-8 -*-
"""
Простая аутентификация. Логин/пароль в data/accounts.txt в открытом виде.
"""
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
ACCOUNTS = os.path.join(DATA_DIR, 'accounts.txt')


def ensure_accounts():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(ACCOUNTS):
        with open(ACCOUNTS, 'w', encoding='utf-8') as f:
            f.write('tester:password\n')


def register_or_login(new=False):
    ensure_accounts()
    login = input('Логин: ').strip()
    pwd = input('Пароль: ').strip()
    with open(ACCOUNTS, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
    users = {}
    for line in lines:
        if ':' in line:
            u, p = line.split(':', 1)
            users[u.strip()] = p.strip()
    if new:
        if login in users:
            print('Пользователь уже существует.')
            return None
        with open(ACCOUNTS, 'a', encoding='utf-8') as f:
            f.write(f"{login}:{pwd}\n")
        print('Аккаунт создан.')
        return login
    else:
        if users.get(login) == pwd:
            print('Успешный вход.')
            return login
        else:
            print('Пароль неверен.')
            return None
