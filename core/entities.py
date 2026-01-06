"""
Базовые модели: дескриптор ClampedInt и модели персонажей.
"""
from typing import Any

class ClampedInt:
    """Дескриптор, ограничивающий значение в диапазоне [min_value, max_value]."""
    def __init__(self, name, min_value=0, max_value=1000):
        # настройка дескриптора
        self.name = '_' + name
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, instance, owner):
        # чтение значения
        if instance is None:
            return self
        return getattr(instance, self.name, self.min_value)

    def __set__(self, instance, value):
        # запись значения
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
    hp = ClampedInt('hp', 0, 600)
    max_hp = ClampedInt('max_hp', 1, 500)

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
        # функция урона
        self.hp = max(0, self.hp - max(0, int(dmg)))

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + int(amount))


"""
Герои: конкретные классы и создание героя по выбору.
"""


class Hero(Character):
    # используем дескрипторы для ресурса, чтобы ограничивать значения
    res = ClampedInt('res', 0, 100)
    max_res = ClampedInt('max_res', 0, 100)

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
    if choice == '1':
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


"""
боссы.
"""


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


"""
боссы.
"""



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
