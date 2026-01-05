# -*- coding: utf-8 -*-
from core.battle import run_battle
from core.save_system import save_state
from core.enemies import create_boss
from core.text_bank import chap5_title, chap5_path, chap5_silence


def run(state):
    if state.get('chapter', 0) < 5:
        print('Сначала пройдите предыдущую главу.')
        return
    print('\n--- Глава 5: Протокол Надзора (Финал) ---')
    print('\n'.join(chap5_title))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap5_path))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap5_silence))
    input('\nНажмите Enter чтобы начать финальный бой...')
    boss = create_boss(5)
    ok = run_battle(state, boss)
    if ok:
        print('\nФинал пройден. Спасибо за игру.')
        state['clarity_points'] = state.get('clarity_points', 0) + 3
        state['chapter'] = 6
        save_state(state)
    else:
        print('Финал не пройден. Можно попробовать ещё.')
