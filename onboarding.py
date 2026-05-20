def read_int(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
        except ValueError:
            pass
        print(f"Bitte eine Zahl zwischen {min_val} und {max_val} eingeben.")


def run_onboarding():
    print("=== Semesterplan – Erstes Setup ===\n")
    count = read_int("Wie viele Kurse belegst du dieses Semester? ", 1, 20)
    modules = []

    for i in range(count):
        print(f"\n--- Kurs {i + 1} ---")
        module = {
            "name":          input("Name: ").strip(),
            "ects":          read_int("ECTS: ", 1, 30),
            "exam_date":     input("Pruefungsdatum (YYYY-MM-DD): ").strip(),
            "difficulty":    read_int("Schwierigkeit (1=leicht, 5=sehr schwer): ", 1, 5),
            "session_types": [],
        }

        types = read_int("Wie viele Veranstaltungstypen? (z.B. VL+GUe = 2): ", 1, 5)
        for j in range(types):
            name = input(f"  Typ {j + 1} (z.B. VL, GUe, Praktikum): ").strip()
            per_week = read_int(f"  {name} pro Woche: ", 1, 7)
            module["session_types"].append({"name": name, "per_week": per_week})

        modules.append(module)

    print("\nSetup gespeichert.")
    return modules
