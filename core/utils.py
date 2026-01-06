# -*- coding: utf-8 -*-
import sys

def wait_enter(prompt='\nНажмите Enter чтобы продолжить...'):
    """Печатает подсказку и ждёт нажатия Enter. Гарантированно сбрасывает буфер вывода."""
    try:
        # print without extra newline (prompt already starts with \n)
        print(prompt, end='', flush=True)
        input()
    except Exception:
        # если ввод недоступен (напр. при тестах), просто пропускаем
        try:
            sys.stdout.flush()
        except Exception:
            pass
