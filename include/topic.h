#pragma once
#include <string>
#include <vector>

struct Topic {
    std::string name;
    std::string course;
    int study_minutes = 0;
    int question_count = 0;
    std::vector<std::string> questions;
};
