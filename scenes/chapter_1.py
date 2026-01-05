# -*- coding: utf-8 -*-
from core.text_bank import (
    platform_after_hero_selected,
    chap1_title,
    chap1_choice1,
    chap1_choice2,
    chap1_choice3,
    chap1_arrival,
    chap1_dispatcher_intro,
    chap1_after_battle,
)
from core.enemies import create_boss
from core.battle import run_battle
from core.artifacts import pop_artifact_from_pool
from core.save_system import save_state


def run(state):
    print('\n--- Глава 1: Депо №0 ---')
    # Вступление: заголовок + платформенная сцена (подставляем имя героя)
    hero_name = state.get('hero', {}).get('name', 'Герой')
    platform_lines = [ln.replace('<ИМЯ ПЕРСОНАЖА>', hero_name) for ln in platform_after_hero_selected]
    print('\n'.join(chap1_title))
    print('\n'.join(platform_lines))
    input('\nНажмите Enter чтобы продолжить...')

    # Ввод выбора (опции уже показаны в тексте платформы)
    choice = input('Ваш выбор (1/2/3): ').strip()
    if choice not in ('1', '2', '3'):
        print('Некорректный выбор — по умолчанию вы заходите в поезд.')
        choice = '3'

    # Показать полноценный фрагмент из text_bank для выбранного варианта
    if choice == '1':
        print('\n'.join(chap1_choice1))
    elif choice == '2':
        print('\n'.join(chap1_choice2))
    else:
        print('\n'.join(chap1_choice3))
    input('\nНажмите Enter чтобы продолжить...')

    # Прибытие на депо — общий фрагмент
    print('\n'.join(chap1_arrival))
    input('\nНажмите Enter чтобы продолжить...')

    # Перед боем показываем вступление диспетчера
    print('\n'.join(chap1_dispatcher_intro))
    input('\nНажмите Enter чтобы начать бой...')
    boss = create_boss(1)
    ok = run_battle(state, boss)
    if ok:
        # Печатаем пост-боевой фрагмент
        print('\n'.join(chap1_after_battle))
        print('>> ГЛАВА 1 ПРОЙДЕНА')
        state['clarity_points'] = state.get('clarity_points', 0) + 2
        # Выдать ровно один артефакт вне зависимости от выбора
        art = pop_artifact_from_pool()
        if art:
            # сохраняем только один
            state.setdefault('artifacts', []).append(art)
            print('>> ПОЛУЧЕН АРТЕФАКТ:', art.get('name'))
        state['chapter'] = 2
        save_state(state)
    else:
        print('Вы не прошли главу 1. Можно попробовать ещё раз в меню сохранений.')
