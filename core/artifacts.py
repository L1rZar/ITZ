"""
Артефакты: пул, постоянные и временные эффекты.
"""

import json
import os
import random
from typing import List

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
POOL_FILE = os.path.join(DATA_DIR, "artifacts_pool.json")

DEFAULT_POOL = [
    {"id": "perm_hp_20", "name": "Пыль депо", "type": "perm", "desc": "+20 к max HP"},
    {"id": "perm_dmg_2", "name": "Осколок табло", "type": "perm", "desc": "+2 к урону"},
    {"id": "cons_medkit", "name": "Аптечка", "type": "cons", "desc": "+35 HP"},
]


def ensure_pool_loaded():
    """Создать файл пула артефактов, если его ещё нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(POOL_FILE):
        with open(POOL_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_POOL, f, ensure_ascii=False, indent=2)


def load_pool() -> List[dict]:
    """Загрузить пул артефактов. Удалить дубликаты id."""
    ensure_pool_loaded()
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool = json.load(f)

    seen = set()
    fixed = []
    duplicates = []
    for art in pool:
        aid = art.get("id")
        if aid in seen:
            duplicates.append(aid)
            continue
        seen.add(aid)
        fixed.append(art)

    if duplicates:
        save_pool(fixed)
        return fixed

    return pool


def save_pool(pool: List[dict]):
    """Сохранить пул артефактов."""
    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)


def _ensure_non_empty_pool() -> List[dict]:
    pool = load_pool()
    if not pool:
        pool = DEFAULT_POOL[:]
        save_pool(pool)
    return pool


def pop_artifact_from_pool():
    """Вытянуть первый артефакт из пула."""
    pool = _ensure_non_empty_pool()
    art = pool.pop(0)
    save_pool(pool)
    return art


def pop_random_consumable_from_pool():
    """
    Вытянуть случайный расходник (type == 'cons') из пула.
    Если расходников нет, вернуть обычный pop_artifact_from_pool().
    """
    pool = _ensure_non_empty_pool()
    cons_indices = [i for i, a in enumerate(pool) if a.get("type") == "cons"]

    if not cons_indices:
        return pop_artifact_from_pool()

    idx = random.choice(cons_indices)
    art = pool.pop(idx)
    save_pool(pool)
    return art


def pop_artifact_by_pool_index(index: int):
    """Вытянуть артефакт по индексу в пуле."""
    pool = _ensure_non_empty_pool()
    if index < 0 or index >= len(pool):
        return None
    art = pool.pop(index)
    save_pool(pool)
    return art


def choose_permanent_artifact(state):
    """
    Выбрать постоянный артефакт из пула (через консоль).
    Добавить его в state['permanent_artifacts'].
    """
    pool = load_pool()
    perms = [(i, a) for i, a in enumerate(pool) if a.get("type") == "perm"]

    if not perms:
        print("В пуле нет постоянных артефактов.")
        return None

    print("Доступные постоянные артефакты:")
    for idx, art in perms:
        name = art.get("name", "Безымянный")
        desc = art.get("desc", "(нет описания)")
        print(f"{idx + 1} - {name} - {desc}")

    choice = input("Ваш выбор (номер) или Enter для пропуска: ").strip()
    if not choice:
        return None

    try:
        num = int(choice) - 1
    except ValueError:
        print("Некорректный ввод.")
        return None

    indices = [p[0] for p in perms]
    if num < 0 or num >= len(indices):
        print("Некорректный выбор.")
        return None

    pool_index = indices[num]
    art = pop_artifact_by_pool_index(pool_index)
    if not art:
        print("Не удалось взять артефакт из пула.")
        return None

    state.setdefault("permanent_artifacts", []).append(art)
    print("Вы выбрали постоянный артефакт:", art.get("name"))
    print("Описание:", art.get("desc", "Описание отсутствует"))
    return art


def return_artifacts_to_pool(arts: List[dict]):
    """Вернуть список артефактов обратно в пул."""
    if not arts:
        return
    pool = load_pool()
    pool.extend(arts)
    save_pool(pool)


def apply_permanent_effects(hero, artifact):
    """
    Применить перманентный артефакт к герою.
    Флаги и поля соответствуют текущей логике игры.
    """
    if not hasattr(hero, "flags"):
        hero.flags = {}

    aid = artifact.get("id")

    if aid == "perm_hp_20":
        hero.max_hp += 20
        hero.hp = min(hero.hp + 20, hero.max_hp)

    if aid == "perm_dmg_2":
        if hasattr(hero, "base_damage"):
            hero.base_damage += 2
        else:
            hero.base_dmg = getattr(hero, "base_dmg", 0) + 2

    if aid == "perm_res_regen_1":
        hero.res = getattr(hero, "res", 0) + 1

    if aid == "perm_first_debuff_minus1":
        hero.flags["first_debuff_shorter"] = True

    if aid == "perm_force_skill_once":
        hero.flags["force_skill_once"] = True

    if aid == "perm_cleanse_once":
        hero.flags["cleanse_once"] = True

    if aid == "perm_heal_bonus":
        hero.flags["heal_bonus_pct"] = hero.flags.get("heal_bonus_pct", 0) + 10

    if aid == "perm_rage_10":
        hero.flags["rage_10"] = True

    if aid == "perm_start_barrier":
        hero.flags["start_barrier"] = hero.flags.get("start_barrier", 0) + 10

    if aid == "perm_buff_positive_plus1":
        hero.flags["buff_positive_plus1"] = True

    if aid == "perm_max_res_plus5":
        hero.max_res = getattr(hero, "max_res", 0) + 5
        if hasattr(hero, "res"):
            hero.res = min(hero.res, hero.max_res)

    if aid == "perm_heal_on_skill_2":
        hero.flags["heal_on_skill_2"] = True

    if aid == "perm_ignore_first_debuff":
        hero.flags["ignore_first_debuff"] = True

    if aid == "perm_dmg_plus1_3turns":
        hero.flags["dmg_plus1_3turns"] = 3

    if aid == "perm_safe_regen_2":
        hero.flags["safe_regen_2"] = True


def use_temporary_artifact(hero, state):
    """
    Использовать один расходуемый артефакт из state['artifacts'].
    Возвращает словарь с эффектом (enemy_dmg_down, hero_dmg_up_pct, cleanse и т.п.).
    """
    pool = state.get("artifacts", [])
    if not pool:
        print("У вас нет артефактов.")
        return None

    print("Ваши артефакты:")
    for i, a in enumerate(pool):
        print(f"{i + 1} - {a.get('name')} ({a.get('id')})")

    choice = input("Выберите номер или Enter для отмены: ").strip()
    if not choice:
        return None

    try:
        idx = int(choice) - 1
    except ValueError:
        print("Некорректный ввод.")
        return None

    if idx < 0 or idx >= len(pool):
        print("Некорректный номер.")
        return None

    art = pool.pop(idx)
    aid = art.get("id")
    result = {"used": True}

    if aid == "cons_medkit":
        if hasattr(hero, "heal"):
            hero.heal(35)
        else:
            hero.hp = min(getattr(hero, "max_hp", hero.hp), hero.hp + 35)
        print("Аптечка использована. +35 HP")
        result["hp"] = 35

    elif aid == "cons_stim":
        hero.res = min(getattr(hero, "max_res", hero.res), hero.res + 4)
        print("Стимулятор использован. +4 RES")
        result["res"] = 4

    elif aid == "cons_tonic":
        print("Тоник использован. Враг наносит меньше урона 3 хода.")
        result["enemy_dmg_down"] = 0.85
        result["turns"] = 3

    elif aid == "cons_spray":
        print("Спрей использован. Ваш урон выше 3 хода.")
        result["hero_dmg_up_pct"] = 15
        result["turns"] = 3

    elif aid == "cons_appeal":
        if not hasattr(hero, "flags"):
            hero.flags = {}
        hero.flags["cleanse_once_used"] = True
        print("Экстренная апелляция использована. Негатив будет очищен.")
        result["cleanse"] = True

    else:
        print("Артефакт использован, но особого эффекта не даёт.")

    state["artifacts"] = pool
    return result
