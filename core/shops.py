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


def open_special_terminal(state):
    """Одноразовый автомат со скидкой для исключительных.
    Позволяет купить временный за 1 ОЯ и постоянный за 3 ОЯ (один раз).
    Сохраняет факт использования в state['flags']['special_terminal_used'].
    """
    used = state.get('flags', {}).get('special_terminal_used')
    if used:
        print('Специальное предложение уже использовано.')
        return
    cp = state.get('clarity_points', 0)
    print('Специальное предложение доступно! Баланс ОЯ:', cp)
    print('1 — Временный артефакт за 1 ОЯ')
    print('2 — Постоянный артефакт за 3 ОЯ')
    print('0 — Выйти')
    choice = input('Ваш выбор: ').strip()
    if choice == '1' and cp >= 1:
        art = pop_artifact_from_pool()
        if art:
            state.setdefault('artifacts', []).append(art)
            state['clarity_points'] = cp - 1
            print('Получен временный артефакт:', art.get('name'))
            state.setdefault('flags', {})['special_terminal_used'] = True
        else:
            print('Артефактов в пуле нет.')
    elif choice == '2' and cp >= 3:
        art = pop_artifact_from_pool()
        if art:
            state.setdefault('artifacts', []).append(art)
            state['clarity_points'] = cp - 3
            print('Получен постоянный артефакт:', art.get('name'))
            state.setdefault('flags', {})['special_terminal_used'] = True
        else:
            print('Артефактов в пуле нет.')
    else:
        print('Неверный выбор или недостаточно ОЯ.')
