# -*- coding: utf-8 -*-
"""
Базовые модели: дескриптор ClampedInt и простые модели персонажей.
"""
from typing import Any


class ClampedInt:
    """Дескриптор, ограничивающий значение в диапазоне [min_value, max_value]."""
    def __init__(self, name, min_value=0, max_value=9999):
        self.name = '_' + name
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, self.min_value)

    def __set__(self, instance, value):
        try:
            v = int(value)
        except (TypeError, ValueError):
            v = self.min_value
        if v < self.min_value:
            v = self.min_value
        if v > self.max_value:
            v = self.max_value
        setattr(instance, self.name, v)


class Character:
    """Базовый класс для героя и врага."""
    hp = ClampedInt('hp', 0, 9999)
    max_hp = ClampedInt('max_hp', 1, 9999)

    def __init__(self, name: str, max_hp: int, base_damage: int):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.base_damage = base_damage
        # эффекты: список словарей {name, kind, turns, params}
        self.effects = []

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    @property
    def hp_percent(self) -> float:
        try:
            return self.hp / self.max_hp * 100
        except Exception:
            return 0.0

    def apply_damage(self, dmg: int):
        # простая функция урона
        self.hp = max(0, self.hp - max(0, int(dmg)))

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + int(amount))
