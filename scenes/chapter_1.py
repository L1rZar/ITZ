# -*- coding: utf-8 -*-
"""
Глава 1: Депо №0.
"""

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
from core.utils import wait_enter


def run(state):
    """
    Проиграть главу 1, если она ещё не пройдена.
    В конце успешного боя выставляет chapter = 2.
    """
    if state.get("chapter", 0) < 1:
        print("Сначала пройдите интро.")
        return
    if state.get("chapter", 0) > 1:
        # глава уже пройдена
        return

    print("\n--- Глава 1: Депо №0 ---")

    hero_name = state.get("hero", {}).get("name", "Герой")
    platform_lines = [
        line.replace("<ИМЯ ПЕРСОНАЖА>", hero_name)
        for line in platform_after_hero_selected
    ]

    print("\n".join(chap1_title))
    print("\n".join(platform_lines))
    wait_enter()

    choice = input("Ваш выбор (1/2/3): ").strip()
    if choice not in ("1", "2", "3"):
        print("Некорректный выбор — по умолчанию вы заходите в поезд.")
        choice = "3"

    if choice == "1":
        print("\n".join(chap1_choice1))
    elif choice == "2":
        print("\n".join(chap1_choice2))
    else:
        print("\n".join(chap1_choice3))
    wait_enter()

    print("\n".join(chap1_arrival))
    wait_enter()

    print("\n".join(chap1_dispatcher_intro))
    wait_enter("\nНажмите Enter чтобы начать бой...")

    boss = create_boss(1)
    ok = run_battle(state, boss)
    if ok:
        print("\n".join(chap1_after_battle))
        print(">> ГЛАВА 1 ПРОЙДЕНА")
        state["clarity_points"] = state.get("clarity_points", 0) + 2

        art = pop_artifact_from_pool()
        if art:
            state.setdefault("artifacts", []).append(art)
            print(">> ПОЛУЧЕН АРТЕФАКТ:", art.get("name"))

        state["chapter"] = 2
        save_state(state)
    else:
        print("Вы не прошли главу 1. Можно попробовать ещё раз позже.")
