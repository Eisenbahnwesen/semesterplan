from datetime import date


def run_checkin(modules, logs):
    week = date.today().isocalendar()[1]
    print(f"\n=== Wochen-Check-in (KW {week}) ===\n")

    for module in modules:
        print(f"--- {module['name']} ---")
        attended = []

        for st in module["session_types"]:
            ans = input(f"  {st['name']} ({st['per_week']}x/Woche) besucht? (j/n): ").strip().lower()
            if ans == "j":
                attended.append(st["name"])

        review = input("  Wiederholung einplanen? (j/n): ").strip().lower() == "j"
        print()

        logs.append({
            "week":          week,
            "module":        module["name"],
            "attended":      attended,
            "review_needed": review,
        })
