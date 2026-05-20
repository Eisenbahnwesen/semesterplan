from datetime import date
from collections import defaultdict


def run_checkin(modules, logs):
    week = date.today().isocalendar()[1]
    print(f"\n=== Wochen-Check-in (KW {week}) ===\n")

    _check_attendance(modules, logs, week)
    _check_tasks(modules, logs, week)


# ── Anwesenheit ──────────────────────────────────────────────────────────────

def _check_attendance(modules, logs, week):
    # Gruppiere Sessions nach Tag über alle Module
    day_plan = defaultdict(list)
    for module in modules:
        for session in module.get("sessions", []):
            day_plan[session["day"]].append((module["name"], session["type"]))

    if not day_plan:
        return

    attended_map = {}  # (modul, typ) → True/False

    print("-- Anwesenheit --")
    for day, sessions in sorted(day_plan.items(), key=_day_order):
        # Bei geteilten Modulen Kontext anzeigen
        labels = []
        for m, t in sessions:
            module = next((mod for mod in modules if mod["name"] == m), {})
            linked = module.get("linked_to", [])
            if linked:
                labels.append(f"{m} {t} (zusammen mit {', '.join(linked)})")
            else:
                labels.append(f"{m} {t}")

        print(f"\n{day}: {', '.join(labels)}")
        ans = _ask("  Warst du wie geplant da? (j/n/t=teilweise): ", ["j", "n", "t"])

        if ans == "j":
            for key in sessions:
                attended_map[key] = True
        elif ans == "n":
            for key in sessions:
                attended_map[key] = False
        else:
            for modul_name, stype in sessions:
                a = _ask(f"    {modul_name} {stype}? (j/n): ", ["j", "n"])
                attended_map[(modul_name, stype)] = (a == "j")

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
            "review_needed": False,
            "tasks_done":    {},
        })


# ── Aufgaben & Reminder ──────────────────────────────────────────────────────

def _check_tasks(modules, logs, week):
    has_tasks = any(module.get("tasks") for module in modules)
    if not has_tasks:
        return

    print("-- Aufgaben & Reminder --")
    for module in modules:
        tasks = module.get("tasks", [])
        if not tasks:
            continue

        for task in tasks:
            if not task.get("weekly"):
                continue

            desc     = task["description"]
            time_str = f" (~{task['time']})" if task["time"] else ""
            days_str = f" [{', '.join(task['days'])}]" if task["days"] else ""
            deadline = f" – Deadline: {task['deadline']}" if task["deadline"] else ""

            prompt = f"[{module['name']}] {desc}{days_str}{time_str}{deadline} → erledigt? (j/n): "
            ans = _ask(prompt, ["j", "n"])

            # In letzten Log-Eintrag des Moduls speichern
            for log in reversed(logs):
                if log["module"] == module["name"] and log["week"] == week:
                    log["tasks_done"][desc] = (ans == "j")
                    break

    # Wiederholung separat
    print()
    print("-- Wiederholung --")
    for module in modules:
        ans = _ask(f"[{module['name']}] Wiederholung einplanen? (j/n): ", ["j", "n"])
        for log in reversed(logs):
            if log["module"] == module["name"] and log["week"] == week:
                log["review_needed"] = (ans == "j")
                break


# ── Hilfsfunktionen ──────────────────────────────────────────────────────────

def _ask(prompt, valid):
    while True:
        ans = input(prompt).strip().lower()
        if ans in valid:
            return ans
        print(f"  Bitte {'/'.join(valid)} eingeben.")


def _day_order(item):
    order = {"Montag": 0, "Dienstag": 1, "Mittwoch": 2, "Donnerstag": 3, "Freitag": 4}
    return order.get(item[0], 99)
