from datetime import date

DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]


def read_int(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
        except ValueError:
            pass
        print(f"Bitte eine Zahl zwischen {min_val} und {max_val} eingeben.")


def read_date(prompt):
    from datetime import datetime
    while True:
        val = input(prompt).strip()
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("Format muss YYYY-MM-DD sein, z.B. 2026-07-23")


def read_day(prompt):
    print(prompt)
    for i, day in enumerate(DAYS, 1):
        print(f"  {i}) {day}")
    idx = read_int("Tag: ", 1, len(DAYS))
    return DAYS[idx - 1]


def run_onboarding():
    print("=== Semesterplan – Erstes Setup ===\n")
    count = read_int("Wie viele Kurse belegst du dieses Semester? ", 1, 20)
    modules = []

    for i in range(count):
        print(f"\n--- Kurs {i + 1} ---")
        module = {
            "name":       input("Name: ").strip(),
            "ects":       read_int("ECTS: ", 1, 30),
            "exam_date":  read_date("Pruefungsdatum (YYYY-MM-DD): "),
            "difficulty": read_int("Schwierigkeit (1=leicht, 5=sehr schwer): ", 1, 5),
            "start_week": date.today().isocalendar()[1],
            "sessions":   [],
        }

        count_types = read_int("Wie viele Veranstaltungstypen? (z.B. VL+GUe = 2): ", 1, 5)
        for j in range(count_types):
            stype = input(f"  Typ {j + 1} (z.B. VL, GUe, Praktikum): ").strip()
            day = read_day(f"  {stype} – an welchem Tag?")
            module["sessions"].append({"type": stype, "day": day})

        modules.append(module)
        print(f"  -> {module['name']} gespeichert.")

    print("\nSetup gespeichert.")
    return modules
