#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Автотест: автоматическое прохождение нескольких глав игры.

Запускает регистрацию нового игрока, выбор героя и последовательно вызывает
сцены (intro, chapter_1..N), подавая автоматические ответы (в основном — '1').
"""
import time
import builtins
import sys
import os

# Ensure repo root is on sys.path when running the script directly
sys.path.insert(0, os.getcwd())

from core import auth, save_system
from scenes import intro, chapter_1, chapter_2, chapter_3


def run_autoplay(chapters: int = 3):
    login = f"autotest_{int(time.time())}"
    pwd = "pass"
    # подготовим поток ответов: регистрация (login, pwd), выбор героя ('1'),
    # затем много атак '1' для каждой главы
    answers = [login, pwd, '1'] + ['1'] * (40 * chapters)
    it = iter(answers)

    old_input = builtins.input
    builtins.input = lambda prompt='': next(it, '1')
    try:
        user = auth.register_or_login(new=True)
        if not user:
            print('Регистрация не удалась')
            return
        state = save_system.create_new_state(user)
        intro.run(state)
        if chapters >= 1:
            chapter_1.run(state)
        if chapters >= 2:
            chapter_2.run(state)
        if chapters >= 3:
            chapter_3.run(state)

        print('Autoplay finished. Current chapter:', state.get('chapter'))
        print('State saved to:', f"data/players/{user}.json")
    finally:
        builtins.input = old_input


if __name__ == '__main__':
    run_autoplay(3)
