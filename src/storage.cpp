#include "storage.h"
#include <nlohmann/json.hpp>
#include <fstream>
#include <iostream>

using json = nlohmann::json;

bool load_data(const std::string& path,
               std::vector<Module>& modules,
               std::vector<WeekLog>& logs)
{
    std::ifstream f(path);
    if (!f.is_open()) return false;

    json j;
    f >> j;

    for (const auto& m : j["modules"]) {
        Module mod;
        mod.name       = m["name"];
        mod.ects       = m["ects"];
        mod.exam_date  = m["exam_date"];
        mod.difficulty = m["difficulty"];
        for (const auto& st : m["session_types"])
            mod.session_types.push_back({st["name"], st["per_week"]});
        modules.push_back(mod);
    }

    for (const auto& l : j["logs"]) {
        WeekLog log;
        log.week          = l["week"];
        log.module        = l["module"];
        log.review_needed = l["review_needed"];
        for (const auto& a : l["attended"])
            log.attended.push_back(a.get<std::string>());
        logs.push_back(log);
    }

    return true;
}

void save_data(const std::string& path,
               const std::vector<Module>& modules,
               const std::vector<WeekLog>& logs)
{
    json j;
    j["modules"] = json::array();
    for (const auto& m : modules) {
        json jm;
        jm["name"]       = m.name;
        jm["ects"]       = m.ects;
        jm["exam_date"]  = m.exam_date;
        jm["difficulty"] = m.difficulty;
        jm["session_types"] = json::array();
        for (const auto& st : m.session_types)
            jm["session_types"].push_back({{"name", st.name}, {"per_week", st.per_week}});
        j["modules"].push_back(jm);
    }

    j["logs"] = json::array();
    for (const auto& l : logs) {
        json jl;
        jl["week"]          = l.week;
        jl["module"]        = l.module;
        jl["review_needed"] = l.review_needed;
        jl["attended"]      = l.attended;
        j["logs"].push_back(jl);
    }

    std::ofstream f(path);
    f << j.dump(2) << "\n";
}
