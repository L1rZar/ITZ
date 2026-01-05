# -*- coding: utf-8 -*-
"""
Простейший магазин "Терминал компенсаций".
"""
from .artifacts import pop_artifact_from_pool


def open_terminal(state):
    cp = state.get('clarity_points', 0)
    print(f'Баланс ОЯ: {cp}')
    print('1 — Обменять 2 ОЯ на временный артефакт')
    print('2 — Обменять 4 ОЯ на постоянный артефакт')
    print('0 — Выйти')
    choice = input('Ваш выбор: ').strip()
    if choice == '1' and cp >= 2:
        art = pop_artifact_from_pool()
        state.setdefault('artifacts', []).append(art)
        state['clarity_points'] = cp - 2
        print('Получен артефакт:', art['name'])
    elif choice == '2' and cp >= 4:
        art = pop_artifact_from_pool()
        state.setdefault('artifacts', []).append(art)
        state['clarity_points'] = cp - 4
        print('Получен постоянный артефакт:', art['name'])
    else:
        print('Неверный выбор или недостаточно ОЯ.')
