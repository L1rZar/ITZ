# -*- coding: utf-8 -*-
"""
Герои: конкретные классы и фабрика создания героя по выбору.
"""
from .models import Character, ClampedInt


class Hero(Character):
    # используем дескрипторы для ресурса, чтобы ограничивать значения
    res = ClampedInt('res', 0, 9999)
    max_res = ClampedInt('max_res', 0, 9999)

    def __init__(self, name, max_hp, base_damage, resource_name, max_res, start_res, hero_class):
        super().__init__(name, max_hp, base_damage)
        self.resource_name = resource_name
        self.max_res = max_res
        self.res = start_res
        self.hero_class = hero_class
        self.artifacts = []

    @property
    def is_resource_enough(self):
        return self.res > 0


def create_hero(choice: str) -> Hero:
    # Взято из TECH_SPEC (значения упрощены и соответствуют README.md)
    if choice == '1':
        # Саня — ресурс задаём как 50% от max_res
        max_res = 10
        start_res = max(1, int(max_res * 0.5))
        return Hero('Саня', 140, 16, 'Выносливость', max_res, start_res, 'warrior')
    elif choice == '2':
        max_res = 10
        start_res = max(1, int(max_res * 0.5))
        return Hero('Марк', 110, 14, 'Фокус', max_res, start_res, 'archer')
    elif choice == '3':
        max_res = 12
        start_res = max(1, int(max_res * 0.5))
        return Hero('Анфиса', 95, 12, 'Мана', max_res, start_res, 'mage')
    elif choice == '4':
        max_res = 10
        start_res = max(1, int(max_res * 0.5))
        return Hero('Юки', 120, 10, 'Вера', max_res, start_res, 'healer')
    else:
        max_res = 10
        start_res = max(1, int(max_res * 0.5))
        return Hero('Саня', 140, 16, 'Выносливость', max_res, start_res, 'warrior')
