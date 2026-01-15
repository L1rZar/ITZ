"""
система эффектов (дебаффы/баффы).
"""
from typing import Dict


def add_effect(target, name: str, kind: str, turns: int, params: Dict = None):
    # Добавляем эффект в список эффектов цели
    if params is None:
        params = {}
    target.effects.append({'name': name, 'kind': kind, 'turns': turns, 'params': params})


def tick_effects(target):
    # Проходимся по эффектам, уменьшаем длительность и применяем периодические эффекты
    new_effects = []
    for ef in target.effects:
        # Применение эффектов типа poison в начале хода героя
        if ef['name'] == 'poison' and ef['kind'] == 'neg':
            dmg = ef['params'].get('dmg', 4)
            target.apply_damage(dmg)
        ef['turns'] -= 1
        if ef['turns'] > 0:
            new_effects.append(ef)
    target.effects = new_effects


def count_effect(target, name: str) -> int:
    return sum(1 for e in target.effects if e['name'] == name)
