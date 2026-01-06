"""
Меню: новая игра, продолжить, пролог, выход.
"""

from core import auth, save_system
from scenes import intro, chapter_1, chapter_2, chapter_3, chapter_4, chapter_5
from core.artifacts import ensure_pool_loaded
from core.text_bank import prolog_recap, main_menu_text


def main():
    ensure_pool_loaded()
    print("Добро пожаловать в 'За МКАДные ужасы — Часть 2' (консольная версия)")
    while True:
        print("\n".join(main_menu_text))
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            login = auth.register_or_login(new=True)
            if not login:
                continue
            state = save_system.create_new_state(login)
            run_game_loop(state)
            break

        elif choice == "2":
            login = auth.register_or_login(new=False)
            if not login:
                continue
            state = save_system.load_state(login)
            if not state:
                print("Сохранения не найдено. Начните новую игру.")
                continue
            run_game_loop(state)
            break

        elif choice == "3":
            if prolog_recap:
                print("\n" + "\n".join(prolog_recap))
            else:
                print("Пролог недоступен.")
            continue

        elif choice == "0":
            print("Выход. До свидания.")
            return

        else:
            print("Некорректный ввод, попробуйте ещё раз.")


def run_game_loop(state):
    """
    Простой цикл по главам.
    Смотрим на state['chapter'] и запускаем только нужные сцены.
    """
    saved = False
    try:
        current = state.get("chapter", 0)

        # 0 — ещё не было интро и выбора героя
        if current <= 0:
            intro.run(state)
            current = state.get("chapter", current)

        if current <= 1:
            chapter_1.run(state)
            current = state.get("chapter", current)

        if current <= 2:
            chapter_2.run(state)
            current = state.get("chapter", current)

        if current <= 3:
            chapter_3.run(state)
            current = state.get("chapter", current)

        if current <= 4:
            chapter_4.run(state)
            current = state.get("chapter", current)

        if current <= 5:
            chapter_5.run(state)
            current = state.get("chapter", current)

        print("Игра пройдена. Спасибо за игру.")
        saved = True

    except KeyboardInterrupt:
        print("\nПрервано игроком.")

    finally:
        if saved:
            save_system.save_state(state)
            print("Прогресс сохранён.")
        else:
            try:
                save_system.save_state(state)
                print("Игра сохранена при выходе.")
            except Exception:
                print("Не удалось сохранить игру при выходе.")


if __name__ == "__main__":
    main()
