# -*- coding: utf-8 -*-
"""
Глава 3: Матушка Лиги Безопасности.
"""

from core.battle import run_battle
from core.save_system import save_state
from core.enemies import create_boss
from core.utils import wait_enter
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
    """
    Глава 3 с учётом ветки branch из главы 2.
    В конце успешного боя выставляет chapter = 4.
    """
    if state.get("chapter", 0) < 3:
        print("Сначала пройдите предыдущую главу.")
        return
    if state.get("chapter", 0) > 3:
        return

    print("\n--- Глава 3: Матушка Лиги Безопасности ---")

    print("\n".join(chap3_title))
    wait_enter()
    print("\n".join(chap3_symptom1))
    wait_enter()
    print("\n".join(chap3_symptom2))
    wait_enter()
    print("\n".join(chap3_system_call))
    wait_enter()
    print("\n".join(chap3_league_scene))
    wait_enter()
    print("\n".join(chap3_matushka_intro))
    wait_enter("\nНажмите Enter чтобы начать бой...")

    branch = state.get("flags", {}).get("branch")

    if branch == "investigate":
        print(
            "Вы пошли в служебные коридоры, чтобы найти источник. Атмосфера напряжённее."
        )
        boss = create_boss(3)
        boss.base_damage += 2
        boss.max_hp += 10
        boss.hp = boss.max_hp
    else:
        print(
            "Вы следовали официальным процедурам. Система заметно холоднее."
        )
        boss = create_boss(3)

    ok = run_battle(state, boss)
    if ok:
        print("\n".join(chap3_after_battle))
        wait_enter()
        print(">> ГЛАВА 3 ПРОЙДЕНА")
        state["clarity_points"] = state.get("clarity_points", 0) + 2
        state["chapter"] = 4
        save_state(state)
    else:
        print("Глава не пройдена.")
