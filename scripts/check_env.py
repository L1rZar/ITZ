# -*- coding: utf-8 -*-
"""Smoke-test: импортирует ключевые модули и выполняет базовые проверки.
Запуск: python3 scripts/check_env.py
"""
import importlib
import sys
import os
import traceback

# Ensure project root is on sys.path so `core` and `scenes` packages import correctly
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

modules = [
    'core.models', 'core.heroes', 'core.enemies', 'core.battle', 'core.effects',
    'core.artifacts', 'core.inventory', 'core.save_system', 'core.auth', 'core.text_bank',
    'scenes.intro', 'scenes.chapter_1'
]

ok = True
for m in modules:
    try:
        mod = importlib.import_module(m)
        print(f'OK import: {m}')
        # print a small sample for text_bank
        if m == 'core.text_bank':
            tb = mod
            keys = getattr(tb, 'TEXT', None)
            if keys:
                print(' - TEXT keys:', list(keys.keys())[:10])
            else:
                print(' - TEXT mapping not found; checking for prolog_recap...')
                print(' - prolog_recap length:', len(getattr(tb, 'prolog_recap', [])))
    except Exception:
        ok = False
        print(f'ERROR importing {m}:')
        traceback.print_exc()

# Try to load artifacts pool
try:
    from core.artifacts import load_pool, ensure_pool_loaded
    ensure_pool_loaded()
    pool = load_pool()
    print('Artifacts pool length:', len(pool))
except Exception:
    ok = False
    print('ERROR during artifacts pool load:')
    traceback.print_exc()

# Try to create a hero and boss if available
try:
    from core.heroes import create_hero
    from core.enemies import create_boss
    h = create_hero('1')
    b = create_boss(1)
    print('Created hero:', getattr(h, 'name', None))
    print('Created boss:', getattr(b, 'name', None))
except Exception:
    ok = False
    print('ERROR creating hero/boss:')
    traceback.print_exc()

if not ok:
    print('\nSOME CHECKS FAILED')
    sys.exit(2)
print('\nALL CHECKS PASSED')
