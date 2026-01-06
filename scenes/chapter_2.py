# -*- coding: utf-8 -*-
"""
Глава 2: Архив претензий.
"""

from core.enemies import create_boss
from core.battle import run_battle
from core.shops import open_terminal
from core.save_system import save_state
from core.utils import wait_enter
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
    """
    Проиграть главу 2, если она ещё не пройдена.
    В конце успешного боя выставляет chapter = 3 и обрабатывает ветку.
    """
    if state.get("chapter", 0) < 2:
        print("Сначала пройдите предыдущую главу.")
        return
    if state.get("chapter", 0) > 2:
        return

    print("\n--- Глава 2: Архив претензий ---")

    print("\n".join(chap2_title))
    wait_enter()
    print("\n".join(chap2_between))
    wait_enter()
    print("\n".join(chap2_voice_message))
    wait_enter()
    print("\n".join(chap2_door_scene))
    wait_enter()
    print("\n".join(chap2_archive_lead))
    wait_enter()
    print("\n".join(chap2_inside_archive))
    wait_enter()
    print("\n".join(chap2_isk_intro))
    wait_enter("\nНажмите Enter чтобы начать бой...")

    boss = create_boss(2)
    ok = run_battle(state, boss)

    if not ok:
        print("Глава не пройдена.")
        return

    print("\n".join(chap2_after_battle))
    wait_enter()
    print(">> ГЛАВА 2 ПРОЙДЕНА")

    state["clarity_points"] = state.get("clarity_points", 0) + 2
    state["chapter"] = 3
    save_state(state)

    print("Открывается Терминал компенсаций...")
    wait_enter()
    open_terminal(state)
    save_state(state)

    print("\nВы видите следы вмешательства системы. Что делать дальше?")
    print("1 — Подать апелляцию через терминал (мягкий путь)")
    print("2 — Идти искать источник в служебные коридоры (агрессивный путь)")
    branch_choice = input("Ваш выбор: ").strip()

    flags = state.setdefault("flags", {})
    if branch_choice == "1":
        flags["branch"] = "appeal"
        print("Вы выбрали апелляцию. Система зафиксировала ваше действие.")
    elif branch_choice == "2":
        flags["branch"] = "investigate"
        print("Вы выбрали искать источник. Это может быть опасно.")
    else:
        flags["branch"] = "appeal"
        print("Неверный ввод — выбран путь по умолчанию: апелляция.")

    save_state(state)
