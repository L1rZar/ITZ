# -*- coding: utf-8 -*-
"""
Интро и выбор героя.
"""

from core.text_bank import intro, intro_metro_scene, hero_select_text
from core.heroes import create_hero
from core.save_system import save_state
from core.utils import wait_enter


def run(state):
    """
    Показывает вступление и даёт выбрать героя.
    В конце устанавливает state['hero'] и state['chapter'] = 1.
    """
    # если герой уже выбран (chapter >= 1), интро можно пропустить
    if state.get("chapter", 0) >= 1 and "hero" in state:
        return

    print("\n".join(intro))
    wait_enter()
    print("\n".join(intro_metro_scene))
    wait_enter()

    print("\n".join(hero_select_text[:-1]))
    while True:
        choice = input("Ваш выбор: ").strip()
        if choice in ("1", "2", "3", "4"):
            hero = create_hero(choice)
            state["hero"] = {
                "name": hero.name,
                "max_hp": hero.max_hp,
                "hp": hero.hp,
                "base_damage": hero.base_damage,
                "resource_name": hero.resource_name,
                "max_res": hero.max_res,
                "res": hero.res,
                "hero_class": hero.hero_class,
            }
            state["chapter"] = 1
            save_state(state)
            print(f"Вы выбрали: {hero.name}")
            break
        else:
            print("Введите 1–4.")
