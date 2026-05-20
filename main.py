from storage import load_data, save_data
from onboarding import run_onboarding
from checkin import run_checkin
from planner import compute_status, show_status


def main():
    modules, logs = load_data()

    if modules is None:
        modules = run_onboarding()
        save_data(modules, logs)
        print("Beim naechsten Start: Wochen-Check-in.")
        return

    run_checkin(modules, logs)

    status = compute_status(modules, logs)
    show_status(status)

    save_data(modules, logs)


if __name__ == "__main__":
    main()
