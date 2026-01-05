#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой запуск игры.
"""
from core import auth, save_system
from scenes import intro, chapter_1, chapter_2, chapter_3, chapter_4, chapter_5
from core.artifacts import ensure_pool_loaded, return_artifacts_to_pool
from core.text_bank import prolog_recap, main_menu_text


def main():
    ensure_pool_loaded()
    print("Добро пожаловать в 'За МКАДные ужасы — Часть 2' (консольная версия)")
    while True:
        print('\n'.join(main_menu_text))
        choice = input('Ваш выбор: ').strip()
        if choice == '1':
            login = auth.register_or_login(new=True)
            if not login:
                continue
            state = save_system.create_new_state(login)
            run_game(state)
            break
        elif choice == '2':
            login = auth.register_or_login(new=False)
            if not login:
                continue
            state = save_system.load_state(login)
            if not state:
                print('Сохранения не найдено. Начните новую игру.')
                continue
            run_game(state)
            break
        elif choice == '3':
            if prolog_recap:
                print('\n' + '\n'.join(prolog_recap))
            else:
                print('Пролог недоступен.')
            continue
        elif choice == '0':
            print('Выход. До свидания.')
            return
        else:
            print('Некорректный ввод, попробуйте ещё раз.')


def run_game(state):
    saved = False
    try:
        intro.run(state)
        chapter_1.run(state)
        chapter_2.run(state)
        chapter_3.run(state)
        chapter_4.run(state)
        chapter_5.run(state)
        print('Игра пройдена. Спасибо за игру.')
        saved = True
    except KeyboardInterrupt:
        print('\nПрервано игроком.')
    finally:
        if not saved:
            # возврат артефактов в пул если игрок вышел без сохранения
            return_artifacts_to_pool(state.get('artifacts', []))
            print('Сессия завершена без сохранения. Артефакты возвращены в пул.')
        else:
            save_system.save_state(state)
            print('Прогресс сохранён.')


if __name__ == '__main__':
    main()
