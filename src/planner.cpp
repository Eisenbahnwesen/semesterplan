#include "planner.h"
#include <algorithm>
#include <ctime>
#include <iostream>
#include <string>

static int days_until_exam(const std::string& date_str) {
    struct tm t = {};
    t.tm_year  = std::stoi(date_str.substr(0, 4)) - 1900;
    t.tm_mon   = std::stoi(date_str.substr(5, 2)) - 1;
    t.tm_mday  = std::stoi(date_str.substr(8, 2));
    t.tm_isdst = -1;
    time_t exam = mktime(&t);
    time_t now  = time(nullptr);
    double diff = difftime(exam, now);
    return static_cast<int>(diff / 86400.0);
}

static int semester_weeks_elapsed() {
    time_t now = time(nullptr);
    struct tm* t = localtime(&now);
    char buf[4];
    strftime(buf, sizeof(buf), "%V", t);
    // KW 15 = Semesterstart (anpassbar)
    return std::max(atoi(buf) - 14, 1);
}

std::vector<ModuleStatus> compute_status(
    const std::vector<Module>& modules,
    const std::vector<WeekLog>& logs)
{
    int weeks = semester_weeks_elapsed();
    std::vector<ModuleStatus> result;

    for (const auto& m : modules) {
        ModuleStatus s;
        s.name            = m.name;
        s.days_until_exam = days_until_exam(m.exam_date);

        int attended = 0;
        bool review  = false;
        for (const auto& l : logs) {
            if (l.module == m.name) {
                attended += static_cast<int>(l.attended.size());
                if (l.review_needed) review = true;
            }
        }

        int sessions_per_week = 0;
        for (const auto& st : m.session_types)
            sessions_per_week += st.per_week;

        int deficit  = std::max(sessions_per_week * weeks - attended, 0);
        double urgency = (s.days_until_exam > 0)
            ? 100.0 / static_cast<double>(s.days_until_exam)
            : 10.0;

        s.score = (m.ects       * 1.5)
                + (m.difficulty * 2.0)
                + (deficit      * 3.0)
                + (urgency      * 10.0)
                + (review ? 5.0 : 0.0);

        if (s.days_until_exam < 14 || s.score > 40)
            s.priority = "DRINGEND";
        else if (deficit > 2 || s.score > 20)
            s.priority = "ZURUECKGEFALLEN";
        else
            s.priority = "IM PLAN";

        if (s.priority == "DRINGEND")
            s.recommendation = "Sofort aufholen – Pruefung naht!";
        else if (review)
            s.recommendation = "Wiederholung einplanen";
        else if (deficit > 0)
            s.recommendation = std::to_string(deficit) + " verpasste Session(s) nachholen";
        else
            s.recommendation = "Weiter so";

        result.push_back(s);
    }

    std::sort(result.begin(), result.end(),
        [](const ModuleStatus& a, const ModuleStatus& b) {
            return a.score > b.score;
        });

    return result;
}

void show_status(const std::vector<ModuleStatus>& status) {
    std::cout << "\n========== STATUS UPDATE ==========\n";
    for (const auto& s : status) {
        std::cout << "[" << s.priority << "] " << s.name
                  << "  (Pruefung in " << s.days_until_exam << " Tagen)\n"
                  << "  -> " << s.recommendation << "\n\n";
    }
    std::cout << "===================================\n";
}
