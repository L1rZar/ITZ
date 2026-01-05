# -*- coding: utf-8 -*-
from core.text_bank import intro, intro_metro_scene, hero_select_text
from core.heroes import create_hero
from core.save_system import save_state


def run(state):
    # Печатаем вводную сцену (интро) перед выбором персонажа
    # Вступление и сцена метро перед выбором героя
    print('\n'.join(intro))
    input('\nНажмите Enter чтобы продолжить...')
    print('\n'.join(intro_metro_scene))
    input('\nНажмите Enter чтобы продолжить...')
    # Выводим текст выбора героя из text_bank (без последней строки-подсказки)
    print('\n'.join(hero_select_text[:-1]))
    while True:
        ch = input('Ваш выбор: ').strip()
        if ch in ('1','2','3','4'):
            hero = create_hero(ch)
            state['hero'] = {
                'name': hero.name,
                'max_hp': hero.max_hp,
                'hp': hero.hp,
                'base_damage': hero.base_damage,
                'resource_name': hero.resource_name,
                'max_res': hero.max_res,
                'res': hero.res,
                'hero_class': hero.hero_class
            }
            state['chapter'] = 1
            save_state(state)
            print(f'Вы выбрали: {hero.name}')
            break
        else:
            print('Введите 1-4')
