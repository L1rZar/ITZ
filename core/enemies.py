# -*- coding: utf-8 -*-
"""
Враги и боссы.
"""
from .models import Character


class Enemy(Character):
    def __init__(self, name, max_hp, base_damage, special=None):
        super().__init__(name, max_hp, base_damage)
        self.special = special or {}


def create_boss(chapter: int):
    # Создаём босса по главе
    if chapter == 1:
        return Enemy('Диспетчер Нулевого Кольца', 120, 11, {'block_every': 2, 'weakness_turn': 1, 'power_turn':7})
    elif chapter == 2:
        return Enemy('Госпожа Иск', 135, 12, {'block_every':2, 'power_turn':8})
    elif chapter == 3:
        return Enemy('Матушка Лиги Безопасности', 155, 13, {'block_every':2, 'power_turn':9})
    elif chapter == 4:
        return Enemy('Куратор Перезагрузки', 175, 14, {'provocation_every':2, 'power_turn':10})
    else:
        return Enemy('Протокол Надзора', 220, 15, {'power_every':5, 'repeats':3})
