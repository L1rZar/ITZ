"""
Пошаговый бой: герой против босса.
Интерфейс: атака / скилл / инвентарь / артефакты.
"""

from .heroes import Hero
from .enemies import Enemy
from .effects import add_effect, tick_effects, count_effect
from .artifacts import apply_permanent_effects, use_temporary_artifact
from .artifacts import pop_random_consumable_from_pool, choose_permanent_artifact
from .inventory import Inventory


def compute_damage(actor, target, base_mult=1.0):
    """
    Посчитать урон с учётом баффов и дебаффов.
    """
    dmg = int(actor.base_damage * base_mult)

    if count_effect(actor, "weakness") > 0:
        dmg = int(dmg * 0.8)

    for ef in getattr(actor, "effects", []):
        if ef.get("name") == "hero_dmg_up":
            pct = ef.get("params", {}).get("pct", 15)
            try:
                mult = 1.0 + float(pct) / 100.0
            except Exception:
                mult = 1.15
            dmg = int(dmg * mult)

    return max(0, dmg)


def _create_hero_from_state(state) -> Hero:
    """Собрать объект Hero из state['hero']."""
    data = state["hero"]
    hero = Hero(
        data["name"],
        data["max_hp"],
        data["base_damage"],
        data["resource_name"],
        data["max_res"],
        data["res"],
        data["hero_class"],
    )
    hero.hp = data.get("hp", hero.max_hp)
    hero.res = data.get("res", hero.res)
    if not hasattr(hero, "flags"):
        hero.flags = {}
    return hero


def _apply_artifacts_to_hero(hero, state):
    """Надеть на героя артефакты и применить постоянные эффекты."""
    arts = state.get("artifacts", [])[:]
    arts += state.get("permanent_artifacts", [])[:]
    hero.artifacts = arts

    for art in hero.artifacts:
        try:
            apply_permanent_effects(hero, art)
        except Exception:
            pass


def _maybe_choose_extra_permanent(state, hero):
    """После 1-й главы позволять брать ещё один постоянный артефакт перед боем."""
    try:
        if state.get("chapter", 0) >= 2:
            art = choose_permanent_artifact(state)
            if art:
                hero.artifacts.append(art)
                apply_permanent_effects(hero, art)
    except Exception:
        pass


def _show_status(hero, boss):
    """Вывести состояние героя и босса."""
    res_name = getattr(hero, "resource_name", "RES")
    res_val = getattr(hero, "res", None)
    res_max = getattr(hero, "max_res", None)

    if res_val is not None and res_max is not None:
        print(
            f"\n--- Ход героя: {hero.name} "
            f"(HP {hero.hp}/{hero.max_hp}, {res_name} {res_val}/{res_max}) ---"
        )
    else:
        print(f"\n--- Ход героя: {hero.name} (HP {hero.hp}/{hero.max_hp}) ---")

    print(f"--- Враг: {boss.name} (HP {boss.hp}/{boss.max_hp}) ---")


def _hero_turn(hero, boss, state, inv: Inventory):
    """
    Один ход героя.
    Возвращает True, если ход потрачен, False - если нет (например, выход из инвентаря).
    """
    print("1 - Атака")
    print("2 - Скилл")
    print("3 - Инвентарь")
    print("4 - Артефакты")
    choice = input("Действие: ").strip()

    if choice == "1":
        dmg = compute_damage(hero, boss, 1.0)
        boss.apply_damage(dmg)
        print(f"Вы наносите {dmg} урона.")
        return True

    if choice == "2":
        cost = 3
        if hero.hero_class == "warrior":
            mult = 1.8
        elif hero.hero_class == "archer":
            mult = 2.2
        elif hero.hero_class == "mage":
            mult = 1.0
        elif hero.hero_class == "healer":
            mult = 0.0
        else:
            mult = 1.5

        if hero.res < cost:
            print("Недостаточно ресурса.")
            return False

        hero.res -= cost
        dmg = compute_damage(hero, boss, mult)
        boss.apply_damage(dmg)

        if hero.hero_class == "mage":
            add_effect(boss, "poison", "neg", 2, {"dmg": 4})
        if hero.hero_class == "healer":
            hero.heal(25)
            add_effect(hero, "shield", "pos", 1, {})

        print(f"Вы используете скилл и наносите {dmg} урона.")
        return True

    if choice == "3":
        used = inv.open_inventory(hero, boss)
        if not used:
            print("Ход не потрачен.")
            return False
        return True

    if choice == "4":
        res = use_temporary_artifact(hero, state)
        if res:
            if res.get("enemy_dmg_down"):
                turns = res.get("turns", 3)
                mult = res.get("enemy_dmg_down")
                add_effect(boss, "enemy_dmg_down", "neg", turns, {"mult": mult})
            if res.get("hero_dmg_up_pct"):
                turns = res.get("turns", 3)
                pct = res.get("hero_dmg_up_pct")
                add_effect(hero, "hero_dmg_up", "pos", turns, {"pct": pct})
            if res.get("cleanse"):
                hero.effects = [
                    e for e in getattr(hero, "effects", []) if e.get("kind") != "neg"
                ]
        return True

    print("Некорректный ввод, ход пропущен.")
    return True


def _boss_turn(hero, boss):
    """Один ход босса: урон с учётом спецэффектов."""
    print(f"\n--- Ход врага: {boss.name} ---")

    damage = boss.base_damage

    for ef in getattr(boss, "effects", []):
        if ef.get("name") == "enemy_dmg_down":
            mult = ef.get("params", {}).get("mult", 1.0)
            try:
                damage = int(damage * float(mult))
            except Exception:
                pass

    hero.apply_damage(damage)
    print(f"Враг наносит {damage} урона.")


def _regen_resource(hero):
    """Простое восстановление ресурса каждый ход."""
    try:
        if hero.hero_class == "healer":
            regen = 2
        else:
            regen = 1
        hero.res = min(hero.max_res, hero.res + regen)
    except Exception:
        pass


def _save_hero_to_state(hero, state):
    """Сохранить текущие характеристики героя в state."""
    state.setdefault("hero", {})
    state["hero"]["hp"] = hero.hp
    state["hero"]["res"] = hero.res
    state["hero"]["max_hp"] = hero.max_hp
    state["hero"]["base_damage"] = hero.base_damage
    state["artifacts"] = hero.artifacts[:]


def run_battle(state, boss: Enemy):
    """
    Простой бой с возможностью повтора.
    Возвращает True, если босс побеждён.
    """
    hero = _create_hero_from_state(state)

    hero.hp = hero.hp
    hero.res = hero.res

    _save_hero_to_state(hero, state)

    _apply_artifacts_to_hero(hero, state)
    _maybe_choose_extra_permanent(state, hero)

    inv = Inventory(state)
    boss_turns = 0

    while hero.is_alive and boss.is_alive:
        tick_effects(hero)
        tick_effects(boss)
        _regen_resource(hero)

        _show_status(hero, boss)

        spent = _hero_turn(hero, boss, state, inv)
        if not spent:
            continue

        if not boss.is_alive:
            print("\nВраг повержен!")
            state["chapter_completed"] = True
            _save_hero_to_state(hero, state)

            try:
                cons = pop_random_consumable_from_pool()
                if cons:
                    state.setdefault("artifacts", []).append(cons)
                    print(">> ПОЛУЧЕН РАСХОДНИК:", cons.get("name"))
            except Exception:
                pass

            return True

        boss_turns += 1
        _boss_turn(hero, boss)

        if not hero.is_alive:
            print("Вы проиграли бой.")
            print("Повторить бой? 1 - Да, 2 - Нет")
            ans = input("> ").strip()

            if ans == "1":
                try:
                    new_max = max(1, int(boss.max_hp * 0.8))
                    boss.max_hp = new_max
                    boss.hp = boss.max_hp
                    print(f"Максимальное HP босса уменьшено: {boss.max_hp}")
                except Exception:
                    pass
                return run_battle(state, boss)

            state["clarity_points"] = state.get("clarity_points", 0) + 1
            _save_hero_to_state(hero, state)
            return False

    _save_hero_to_state(hero, state)
    return hero.is_alive and not boss.is_alive
