# -*- coding: utf-8 -*-
from core.enemies import create_boss
from core.battle import run_battle
from core.shops import open_terminal
from core.save_system import save_state
from core.text_bank import (
    chap2_title,
    chap2_between,
    chap2_voice_message,
    chap2_door_scene,
    chap2_archive_lead,
    chap2_inside_archive,
    chap2_isk_intro,
    chap2_after_battle,
)


def run(state):
    if state.get('chapter', 0) < 2:
        print('Сначала пройдите предыдущую главу.')
        return
    print('\n--- Глава 2: Архив претензий ---')
    print('\n'.join(chap2_title))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap2_between))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap2_voice_message))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap2_door_scene))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap2_archive_lead))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap2_inside_archive))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(chap2_isk_intro))
    input('\nНажмите Enter чтобы начать бой...')
    boss = create_boss(2)
    ok = run_battle(state, boss)
    if ok:
        print('\n'.join(chap2_after_battle))
        input('\nНажмите Enter чтобы продолжить...')
        print('>> ГЛАВА 2 ПРОЙДЕНА')
        state['clarity_points'] = state.get('clarity_points', 0) + 2
        state['chapter'] = 3
        save_state(state)
        # открыть терминал компенсаций
        print('Открывается Терминал компенсаций...')
        input('\nНажмите Enter чтобы продолжить...')
        open_terminal(state)
        save_state(state)
        # Ветвление сюжета: выбрать дальнейший путь
        print('\nВы видите следы вмешательства системы. Что делать дальше?')
        print('1 — Подать апелляцию через терминал (мягкий путь)')
        print('2 — Идти искать источник в служебные коридоры (агрессивный путь)')
        choice = input('Ваш выбор: ').strip()
        if choice == '1':
            state.setdefault('flags', {})['branch'] = 'appeal'
            print('Вы выбрали апелляцию. Система зафиксировала ваше действие.')
        elif choice == '2':
            state.setdefault('flags', {})['branch'] = 'investigate'
            print('Вы выбрали искать источник. Это может быть опасно.')
        else:
            state.setdefault('flags', {})['branch'] = 'appeal'
            print('Неверный ввод — выбран путь по умолчанию: апелляция.')
        save_state(state)
    else:
        print('Глава не пройдена.')
