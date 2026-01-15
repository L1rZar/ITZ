"""
Глава 4: Куратор Перезагрузки.
"""

from core.battle import run_battle
from core.save_system import save_state
from core.enemies import create_boss
from core.utils import wait_enter
from core.text_bank import (
    chap4_title,
    chap4_between,
    chap4_center,
    chap4_curator_intro,
    chap4_after_battle,
)
from core.shops import open_special_terminal


def run(state):
    """
    Глава 4. Открывает спец-терминал и даёт бой с Куратором.
    В конце успешного боя выставляет chapter = 5.
    """
    if state.get("chapter", 0) < 4:
        print("Сначала пройдите предыдущую главу.")
        return
    if state.get("chapter", 0) > 4:
        return

    print("\n--- Глава 4: Куратор Перезагрузки ---")

    print("\n".join(chap4_title))
    wait_enter()
    print("\n".join(chap4_between))
    wait_enter()

    open_special_terminal(state)
    wait_enter()

    print("\n".join(chap4_center))
    wait_enter()
    print("\n".join(chap4_curator_intro))
    wait_enter("\nНажмите Enter чтобы начать бой...")

    boss = create_boss(4)
    ok = run_battle(state, boss)

    if ok:
        print("\n".join(chap4_after_battle))
        input("\nНажмите Enter чтобы продолжить...")
        print(">> ГЛАВА 4 ПРОЙДЕНА")
        state["clarity_points"] = state.get("clarity_points", 0) + 2
        state["chapter"] = 5
        save_state(state)
    else:
        print("Глава не пройдена.")
