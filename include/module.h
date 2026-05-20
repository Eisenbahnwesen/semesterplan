#pragma once
#include <string>
#include <vector>

struct SessionType {
    std::string name;
    int per_week;
};

struct Module {
    std::string name;
    int ects;
    std::string exam_date;  // "YYYY-MM-DD"
    int difficulty;         // 1-5
    std::vector<SessionType> session_types;
};

struct WeekLog {
    int week;
    std::string module;
    std::vector<std::string> attended;
    bool review_needed;
};
