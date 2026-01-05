# -*- coding: utf-8 -*-
from core.battle import run_battle
from core.save_system import save_state
from core.enemies import create_boss
from core.text_bank import (
    chap3_title,
    chap3_symptom1,
    chap3_symptom2,
    chap3_system_call,
    chap3_league_scene,
    chap3_matushka_intro,
    chap3_after_battle,
)


def run(state):
    if state.get('chapter', 0) < 3:
        print('Сначала пройдите предыдущую главу.')
        return
    print('\n--- Глава 3: Матушка Лиги Безопасности ---')
    print('\n'.join(chap3_title))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap3_symptom1))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap3_symptom2))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap3_system_call))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap3_league_scene))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap3_matushka_intro))
    input('\nНажмите Enter чтобы начать бой...')
    # Учитываем ветвление из главы 2
    branch = state.get('flags', {}).get('branch')
    if branch == 'investigate':
        print('Вы пошли в служебные коридоры, чтобы найти источник. Атмосфера напряжённее.')
        # более сложный босс (усиленный)
        boss = create_boss(3)
        boss.base_damage += 2
        boss.max_hp += 10
        boss.hp = boss.max_hp
    else:
        print('Вы следовали официальным процедурам. Система заметно холоднее.')
        boss = create_boss(3)
    ok = run_battle(state, boss)
    if ok:
        print('\n'.join(chap3_after_battle))
        input('\nНажмите Enter чтобы продолжить...')
        print('>> ГЛАВА 3 ПРОЙДЕНА')
        state['clarity_points'] = state.get('clarity_points', 0) + 2
        state['chapter'] = 4
        save_state(state)
    else:
        print('Глава не пройдена.')
