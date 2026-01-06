# -*- coding: utf-8 -*-
"""
Простейший инвентарь: расходники.
"""


class Inventory:
    def __init__(self, state):
        self.state = state
        # структура state['inventory'] = {"medkit": 1, ...}
        if 'inventory' not in state:
            state['inventory'] = {'medkit': 1}

    def open_inventory(self, hero, boss):
        inv = self.state.get('inventory', {})
        # если инвентарь пуст — не тратить ход
        non_zero = any(v > 0 for v in inv.values())
        if not inv or not non_zero:
            print('Инвентарь пуст.')
            return False

        print('Инвентарь:')
        for k, v in inv.items():
            print(f"{k}: {v}")
        print('1 — Использовать аптечку')
        print('0 — Выйти')
        ch = input('> ').strip()
        if ch == '0':
            # выход из инвентаря не тратит ход
            print('Выход из инвентаря.')
            return False
        if ch == '1':
            if inv.get('medkit', 0) > 0:
                hero.heal(35)
                inv['medkit'] -= 1
                print('+35 HP')
                return True
            else:
                print('У вас нет аптечек.')
                return False

        print('Ничего не происходит.')
        return False
