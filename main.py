import os
from storage import load_data, save_data
from schedule_reader import read_schedule
from checkin import run_checkin
from planner import compute_status, show_status

SCHEDULE_FILE = "Stundenplan.xlsx"
DATA_FILE     = "semester.json"


def main():
    # Stundenplan immer frisch aus Excel lesen (Aenderungen wirken sofort)
    if not os.path.exists(SCHEDULE_FILE):
        print(f"'{SCHEDULE_FILE}' nicht gefunden.")
        print("Erstelle zuerst die Vorlage mit: python create_template.py")
        return

    modules = read_schedule(SCHEDULE_FILE)
    _, logs = load_data()
    if logs is None:
        logs = []

    run_checkin(modules, logs)

    status = compute_status(modules, logs)
    show_status(status)

    save_data(modules, logs)


if __name__ == "__main__":
    main()
