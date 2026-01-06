# -*- coding: utf-8 -*-
"""
Глава 5: Протокол Надзора (финал).
"""

from core.battle import run_battle
from core.save_system import save_state
from core.enemies import create_boss
from core.utils import wait_enter
from core.text_bank import chap5_title, chap5_path, chap5_silence


def run(state):
    """
    Финальная глава.
    В конце успешного боя выставляет chapter = 6.
    """
    if state.get("chapter", 0) < 5:
        print("Сначала пройдите предыдущую главу.")
        return
    if state.get("chapter", 0) > 5:
        return

    print("\n--- Глава 5: Протокол Надзора (Финал) ---")

    print("\n".join(chap5_title))
    wait_enter()
    print("\n".join(chap5_path))
    wait_enter()
    print("\n".join(chap5_silence))
    wait_enter("\nНажмите Enter чтобы начать финальный бой...")

    boss = create_boss(5)
    ok = run_battle(state, boss)

    if ok:
        print("\nФинал пройден. Спасибо за игру.")
        state["clarity_points"] = state.get("clarity_points", 0) + 3
        state["chapter"] = 6
        save_state(state)
    else:
        print("Финал не пройден. Можно попробовать ещё.")
