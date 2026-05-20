#include "module.h"
#include "storage.h"
#include "onboarding.h"
#include "checkin.h"
#include "planner.h"
#include <filesystem>
#include <iostream>
#include <vector>

const std::string DATA_FILE = "semester.json";

int main() {
    std::vector<Module> modules;
    std::vector<WeekLog> logs;

    if (!std::filesystem::exists(DATA_FILE)) {
        std::cout << "=== Semesterplan – Erstes Setup ===\n\n";
        modules = run_onboarding();
        save_data(DATA_FILE, modules, logs);
        std::cout << "\nSetup gespeichert in semester.json.\n";
        std::cout << "Beim naechsten Start: Wochen-Check-in.\n";
        return 0;
    }

    if (!load_data(DATA_FILE, modules, logs)) {
        std::cerr << "Fehler beim Laden von " << DATA_FILE << "\n";
        return 1;
    }

    run_checkin(modules, logs);

    auto status = compute_status(modules, logs);
    show_status(status);

    save_data(DATA_FILE, modules, logs);
    return 0;
}
