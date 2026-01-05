# -*- coding: utf-8 -*-
from core.battle import run_battle
from core.save_system import save_state
from core.enemies import create_boss
from core.text_bank import (
    chap4_title,
    chap4_between,
    chap4_center,
    chap4_curator_intro,
    chap4_after_battle,
)


def run(state):
    if state.get('chapter', 0) < 4:
        print('Сначала пройдите предыдущую главу.')
        return
    print('\n--- Глава 4: Куратор Перезагрузки ---')
    print('\n'.join(chap4_title))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap4_between))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap4_center))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap4_curator_intro))
    input('\nНажмите Enter чтобы начать бой...')
    boss = create_boss(4)
    ok = run_battle(state, boss)
    if ok:
        print('\n'.join(chap4_after_battle))
        input('\nНажмите Enter чтобы продолжить...')
        print('>> ГЛАВА 4 ПРОЙДЕНА')
        state['clarity_points'] = state.get('clarity_points', 0) + 2
        state['chapter'] = 5
        save_state(state)
    else:
        print('Глава не пройдена.')
