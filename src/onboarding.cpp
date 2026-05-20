#include "onboarding.h"
#include <iostream>
#include <limits>
#include <string>

static std::string read_line(const std::string& prompt) {
    std::string s;
    std::cout << prompt;
    std::getline(std::cin, s);
    return s;
}

static int read_int(const std::string& prompt, int min_val, int max_val) {
    int val;
    while (true) {
        std::cout << prompt;
        if (std::cin >> val && val >= min_val && val <= max_val) {
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            return val;
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Bitte Zahl zwischen " << min_val << " und " << max_val << " eingeben.\n";
    }
}

std::vector<Module> run_onboarding() {
    int count = read_int("Wie viele Kurse belegst du dieses Semester? ", 1, 20);
    std::vector<Module> modules;

    for (int i = 0; i < count; ++i) {
        std::cout << "\n--- Kurs " << (i + 1) << " ---\n";
        Module m;
        m.name       = read_line("Name: ");
        m.ects       = read_int("ECTS: ", 1, 30);
        m.exam_date  = read_line("Pruefungsdatum (YYYY-MM-DD): ");
        m.difficulty = read_int("Schwierigkeit (1=leicht, 5=sehr schwer): ", 1, 5);

        int types = read_int("Wie viele Veranstaltungstypen? (z.B. VL+GUe = 2): ", 1, 5);
        for (int j = 0; j < types; ++j) {
            SessionType st;
            std::cout << "  Typ " << (j + 1) << " (z.B. VL, GUe, Praktikum): ";
            std::getline(std::cin, st.name);
            st.per_week = read_int("  " + st.name + " pro Woche: ", 1, 7);
            m.session_types.push_back(st);
        }
        modules.push_back(m);
    }
    return modules;
}
