# -*- coding: utf-8 -*-
"""
Артефакты: пул, применение постоянных и временных эффектов.
"""
import json
import os
from typing import List

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
POOL_FILE = os.path.join(DATA_DIR, 'artifacts_pool.json')


DEFAULT_POOL = [
    {"id": "perm_hp_20", "name": "Пыль депо", "type": "perm", "desc": "+20 к max HP"},
    {"id": "perm_dmg_2", "name": "Осколок табло", "type": "perm", "desc": "+2 к урону"},
    {"id": "cons_medkit", "name": "Аптечка", "type": "cons", "desc": "+35 HP"},
]


def ensure_pool_loaded():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(POOL_FILE):
        with open(POOL_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_POOL, f, ensure_ascii=False, indent=2)


def load_pool() -> List[dict]:
    ensure_pool_loaded()
    with open(POOL_FILE, 'r', encoding='utf-8') as f:
        pool = json.load(f)
    # Валидируем уникальность id и фиксируем дубликаты автоматически
    seen = set()
    fixed = []
    duplicates = []
    for art in pool:
        aid = art.get('id')
        if aid in seen:
            duplicates.append(aid)
            continue
        seen.add(aid)
        fixed.append(art)
    if duplicates:
        print(f"[artifacts] Удалены дубликаты id в {POOL_FILE}: {duplicates}")
        save_pool(fixed)
        return fixed
    return pool


def save_pool(pool: List[dict]):
    with open(POOL_FILE, 'w', encoding='utf-8') as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)


def pop_artifact_from_pool():
    pool = load_pool()
    if not pool:
        pool = DEFAULT_POOL[:]
        save_pool(pool)
    art = pool.pop(0)
    save_pool(pool)
    return art


def return_artifacts_to_pool(arts: List[dict]):
    if not arts:
        return
    pool = load_pool()
    pool.extend(arts)
    save_pool(pool)


def apply_permanent_effects(hero, artifact):
    """Применить единичный перманентный артефакт к герою (из экипировки).
    В реальной игре эффекты должны аккуратно храниться в state/flags.
    """
    aid = artifact.get('id')
    if aid == 'perm_hp_20':
        hero.max_hp += 20
        hero.hp = min(hero.hp + 20, hero.max_hp)
    if aid == 'perm_dmg_2':
        if hasattr(hero, 'base_damage'):
            hero.base_damage += 2
        else:
            hero.base_dmg = getattr(hero, 'base_dmg', 0) + 2
    if aid == 'perm_res_regen_1':
        hero.res = getattr(hero, 'res', 0) + 1
    if aid == 'perm_first_debuff_minus1':
        hero.flags['first_debuff_shorter'] = True
    if aid == 'perm_force_skill_once':
        hero.flags['force_skill_once'] = True
    if aid == 'perm_cleanse_once':
        hero.flags['cleanse_once'] = True
    if aid == 'perm_heal_bonus':
        hero.flags['heal_bonus_pct'] = hero.flags.get('heal_bonus_pct', 0) + 10
    if aid == 'perm_rage_10':
        hero.flags['rage_10'] = True
    if aid == 'perm_start_barrier':
        hero.flags['start_barrier'] = hero.flags.get('start_barrier', 0) + 10
    if aid == 'perm_buff_positive_plus1':
        hero.flags['buff_positive_plus1'] = True
    if aid == 'perm_max_res_plus5':
        hero.max_res = getattr(hero, 'max_res', 0) + 5
        if hasattr(hero, 'res'):
            hero.res = min(hero.res, hero.max_res)
    if aid == 'perm_heal_on_skill_2':
        hero.flags['heal_on_skill_2'] = True
    if aid == 'perm_ignore_first_debuff':
        hero.flags['ignore_first_debuff'] = True
    if aid == 'perm_dmg_plus1_3turns':
        hero.flags['dmg_plus1_3turns'] = 3
    if aid == 'perm_safe_regen_2':
        hero.flags['safe_regen_2'] = True


def use_temporary_artifact(hero, state):
    """Интерактивное использование расходника из state['artifacts'].
    Возвращает словарь эффекта при некоторых предметах.
    """
    pool = state.get('artifacts', [])
    if not pool:
        print('У вас нет артефактов.')
        return None
    print('Ваши артефакты:')
    for i, a in enumerate(pool):
        print(f"{i+1} — {a.get('name')} ({a.get('id')})")
    choice = input('Выберите номер для использования или Enter: ').strip()
    if not choice:
        return None
    try:
        idx = int(choice) - 1
        art = pool.pop(idx)
        aid = art.get('id')
        if aid == 'cons_medkit':
            if hasattr(hero, 'heal'):
                hero.heal(35)
            else:
                hero.hp = min(getattr(hero, 'max_hp', hero.hp), hero.hp + 35)
            print('Аптечка использована. +35 HP')
            state['artifacts'] = pool
            return {'used': True, 'hp': 35}
        if aid == 'cons_stim':
            hero.res = min(getattr(hero, 'max_res', hero.res), hero.res + 4)
            print('Стимулятор использован. +4 RES')
            state['artifacts'] = pool
            return {'used': True, 'res': 4}
        if aid == 'cons_tonic':
            print('Тоник использован. Уменьшение урона врага на 15% на 3 хода.')
            state['artifacts'] = pool
            return {'used': True, 'enemy_dmg_down': 0.85, 'turns': 3}
        if aid == 'cons_spray':
            print('Спрей использован. Увеличение урона героя на 15% на 3 хода.')
            state['artifacts'] = pool
            return {'used': True, 'hero_dmg_up_pct': 15, 'turns': 3}
        if aid == 'cons_appeal':
            hero.flags['cleanse_once_used'] = True
            print('Привлечение использовано. Очистка статуса.')
            state['artifacts'] = pool
            return {'used': True, 'cleanse': True}
        # по умолчанию: просто удалён из рюкзака
        state['artifacts'] = pool
        return {'used': True}
    except Exception:
        print('Некорректный выбор.')
        return None
