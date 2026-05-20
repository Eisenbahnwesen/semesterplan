#include "checkin.h"
#include <ctime>
#include <iostream>
#include <string>

static int current_iso_week() {
    time_t t = time(nullptr);
    struct tm* now = localtime(&t);
    char buf[4];
    strftime(buf, sizeof(buf), "%V", now);
    return atoi(buf);
}

void run_checkin(const std::vector<Module>& modules, std::vector<WeekLog>& logs) {
    int week = current_iso_week();
    std::cout << "\n=== Wochen-Check-in (KW " << week << ") ===\n\n";

    for (const auto& m : modules) {
        std::cout << "--- " << m.name << " ---\n";

        WeekLog log;
        log.week          = week;
        log.module        = m.name;
        log.review_needed = false;

        for (const auto& st : m.session_types) {
            std::string ans;
            std::cout << "  " << st.name << " (" << st.per_week
                      << "x/Woche) besucht? (j/n): ";
            std::getline(std::cin, ans);
            if (!ans.empty() && (ans[0] == 'j' || ans[0] == 'J'))
                log.attended.push_back(st.name);
        }

        std::string rev;
        std::cout << "  Wiederholung einplanen? (j/n): ";
        std::getline(std::cin, rev);
        if (!rev.empty() && (rev[0] == 'j' || rev[0] == 'J'))
            log.review_needed = true;

        logs.push_back(log);
        std::cout << "\n";
    }
}
