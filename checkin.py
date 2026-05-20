from datetime import date
from collections import defaultdict


def run_checkin(modules, logs):
    week = date.today().isocalendar()[1]
    print(f"\n=== Wochen-Check-in (KW {week}) ===\n")

    # Gruppiere alle Sessions nach Tag
    # { "Montag": [("Statistik", "VL"), ("OR", "VL")], ... }
    day_plan = defaultdict(list)
    for module in modules:
        for session in module.get("sessions", []):
            day_plan[session["day"]].append((module["name"], session["type"]))

    if not day_plan:
        print("Keine Sessions konfiguriert.")
        return

    attended_map = {}  # (module, type) -> True/False

    for day, sessions in sorted(day_plan.items(), key=_day_order):
        session_labels = ", ".join(f"{m} {t}" for m, t in sessions)
        print(f"{day}: {session_labels}")

        ans = _ask(f"  Warst du wie geplant da? (j/n/t=teilweise): ", ["j", "n", "t"])

        if ans == "j":
            for key in sessions:
                attended_map[key] = True

        elif ans == "n":
            for key in sessions:
                attended_map[key] = False

        else:  # teilweise
            for module_name, stype in sessions:
                a = _ask(f"    {module_name} {stype}? (j/n): ", ["j", "n"])
                attended_map[(module_name, stype)] = (a == "j")

        print()

    # Wiederholungsbedarf pro Modul abfragen
    review_map = {}
    for module in modules:
        ans = _ask(f"Wiederholung fuer {module['name']} einplanen? (j/n): ", ["j", "n"])
        review_map[module["name"]] = (ans == "j")
    print()

    # Logs schreiben
    for module in modules:
        attended = [
            stype
            for (m, stype), ok in attended_map.items()
            if m == module["name"] and ok
        ]
        logs.append({
            "week":          week,
            "module":        module["name"],
            "attended":      attended,
            "review_needed": review_map.get(module["name"], False),
        })


def _ask(prompt, valid):
    while True:
        ans = input(prompt).strip().lower()
        if ans in valid:
            return ans
        print(f"  Bitte {'/'.join(valid)} eingeben.")


def _day_order(item):
    order = {"Montag": 0, "Dienstag": 1, "Mittwoch": 2, "Donnerstag": 3, "Freitag": 4}
    return order.get(item[0], 99)
