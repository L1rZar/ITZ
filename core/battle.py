# -*- coding: utf-8 -*-
"""
Простая пошаговая боевая система "герой vs босс".
Меню: атака/скилл/инвентарь/артефакт.
"""
from .heroes import Hero
from .enemies import Enemy
from .effects import add_effect, tick_effects, count_effect
from .artifacts import apply_permanent_effects, use_temporary_artifact
from .inventory import Inventory
import math


def compute_damage(actor, target, base_mult=1.0):
    dmg = int(actor.base_damage * base_mult)
    # учитываем слабость на атакующем
    if count_effect(actor, 'weakness') > 0:
        dmg = int(dmg * 0.8)
    # бафф урона (поддерживаем параметрический процент)
    for ef in getattr(actor, 'effects', []):
        if ef.get('name') == 'hero_dmg_up':
            pct = ef.get('params', {}).get('pct', 15)
            try:
                mult = 1.0 + float(pct) / 100.0
                dmg = int(dmg * mult)
            except Exception:
                dmg = int(dmg * 1.15)
    return max(0, dmg)


def run_battle(state, boss: Enemy):
    # Простейший бой с мягким таймером и возможностью повтора
    hero_data = state['hero']
    hero = Hero(hero_data['name'], hero_data['max_hp'], hero_data['base_damage'], hero_data['resource_name'], hero_data['max_res'], hero_data['res'], hero_data['hero_class'])
    # Восстановим героя до максимального здоровья перед боем
    hero.hp = hero_data.get('hp', hero.max_hp)
    try:
        hero.hp = hero.max_hp
    except Exception:
        pass
    # Ресурс оставляем таким, какой в `state` (не восстанавливаем до максимума)
    hero.res = hero_data.get('res', getattr(hero, 'res', 0))
    # Обновим state, чтобы отражать восстановление перед боем
    state.setdefault('hero', {})['hp'] = hero.hp
    state['hero']['res'] = hero.res
    hero.artifacts = state.get('artifacts', [])[:]

    # Применяем постоянные эффекты от артефактов (если есть)
    for a in hero.artifacts:
        try:
            apply_permanent_effects(hero, a)
        except Exception:
            pass

    inv = Inventory(state)

    turn = 1
    boss_turns = 0
    while hero.is_alive and boss.is_alive:
        # эффекты в начале хода героя
        tick_effects(hero)
        tick_effects(boss)
        # восстановление ресурса героя каждый ход (по умолчанию +1, у целителя +2)
        try:
            if getattr(hero, 'hero_class', '') == 'healer':
                regen = 2
            else:
                regen = 1
            hero.res = min(hero.max_res, hero.res + regen)
        except Exception:
            pass

        # Показываем также ресурс героя и здоровье босса
        res_name = getattr(hero, 'resource_name', 'RES')
        res_val = getattr(hero, 'res', None)
        res_max = getattr(hero, 'max_res', None)
        if res_val is not None and res_max is not None:
            print('\n--- Ход героя: {} (HP {}/{}, {} {}/{}) ---'.format(hero.name, hero.hp, hero.max_hp, res_name, res_val, res_max))
        else:
            print('\n--- Ход героя: {} (HP {}/{}) ---'.format(hero.name, hero.hp, hero.max_hp))
        print('--- Враг: {} (HP {}/{}) ---'.format(boss.name, boss.hp, boss.max_hp))

        print('1 — Атака')
        print('2 — Скилл')
        print('3 — Инвентарь')
        print('4 — Артефакты')
        choice = input('Действие: ').strip()
        if choice == '1':
            dmg = compute_damage(hero, boss, 1.0)
            boss.apply_damage(dmg)
            print('Вы наносите {} урона.'.format(dmg))
        elif choice == '2':
            # простые скиллы по классу
            cost = 3
            if hero.hero_class == 'warrior':
                mult = 1.8
            elif hero.hero_class == 'archer':
                mult = 2.2
            elif hero.hero_class == 'mage':
                mult = 1.0
            elif hero.hero_class == 'healer':
                mult = 0.0
            else:
                mult = 1.5
            if hero.res >= cost:
                hero.res -= cost
                dmg = compute_damage(hero, boss, mult)
                boss.apply_damage(dmg)
                # дополнительные эффекты
                if hero.hero_class == 'mage':
                    add_effect(boss, 'poison', 'neg', 2, {'dmg': 4})
                if hero.hero_class == 'healer':
                    hero.heal(25)
                    add_effect(hero, 'shield', 'pos', 1, {})
                print('Вы используете скилл и наносите {} урона.'.format(dmg))
            else:
                print('Недостаточно ресурса.')
        elif choice == '3':
            used = inv.open_inventory(hero, boss)
            # если инвентарь пуст и открытие не использовало предмет — не тратить ход
            if not used:
                print('Ход не потрачен.')
                continue
        elif choice == '4':
            res = use_temporary_artifact(hero, state)
            # применение эффектов, возвращённых расходником
            if res:
                if res.get('enemy_dmg_down'):
                    turns = res.get('turns', 3)
                    mult = res.get('enemy_dmg_down')
                    add_effect(boss, 'enemy_dmg_down', 'neg', turns, {'mult': mult})
                if res.get('hero_dmg_up_pct'):
                    turns = res.get('turns', 3)
                    pct = res.get('hero_dmg_up_pct')
                    add_effect(hero, 'hero_dmg_up', 'pos', turns, {'pct': pct})
                if res.get('cleanse'):
                    # убрать негативные эффекты у героя
                    hero.effects = [e for e in getattr(hero, 'effects', []) if e.get('kind') != 'neg']
        else:
            print('Некорректный ввод, ход пропущен.')

        if not boss.is_alive:
            print('\nВраг повержен!')
            state['chapter_completed'] = True
            # сохранить прогресс героя в state
            state.setdefault('hero', {})['hp'] = hero.hp
            state['hero']['res'] = hero.res
            state['hero']['max_hp'] = hero.max_hp
            state['hero']['base_damage'] = hero.base_damage
            state['artifacts'] = hero.artifacts[:]
            return True

        # Ход босса
        boss_turns += 1
        print('\n--- Ход врага: {} ---'.format(boss.name))
        # применение специальных действий босса
        damage = boss.base_damage
        # ранние усиления
        if boss.special.get('power_turn') and boss_turns == boss.special.get('power_turn'):
            damage = int(damage * 1.1)
            print('Враг усиливается!')
        # учёт дебаффов на враге, снижающих его урон
        for ef in getattr(boss, 'effects', []):
            if ef.get('name') == 'enemy_dmg_down':
                mult = ef.get('params', {}).get('mult', 1.0)
                try:
                    damage = int(damage * float(mult))
                except Exception:
                    pass
        hero.apply_damage(damage)
        print('Враг наносит {} урона.'.format(damage))

        if not hero.is_alive:
            print('Вы проиграли бой.')
            # опция повтора
            print('Повторить бой? 1 — Да, 2 — Нет')
            ans = input('> ').strip()
            if ans == '1':
                # повтор боя — восстановим героя из state
                return run_battle(state, boss)
            else:
                # считаем главу проигранной, даём 1 ОЯ
                state['clarity_points'] = state.get('clarity_points', 0) + 1
                # сохранить текущее состояние героя (он мёртв, но сохраняем для логики)
                state.setdefault('hero', {})['hp'] = hero.hp
                state['hero']['res'] = hero.res
                state['artifacts'] = hero.artifacts[:]
                return False

        turn += 1

    # финальное сохранение
    state.setdefault('hero', {})['hp'] = hero.hp
    state['hero']['res'] = hero.res
    state['artifacts'] = hero.artifacts[:]
    return hero.is_alive and not boss.is_alive
