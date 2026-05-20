#pragma once
#include "module.h"
#include <string>
#include <vector>

struct ModuleStatus {
    std::string name;
    std::string priority;       // "DRINGEND", "ZURÜCKGEFALLEN", "IM PLAN"
    int days_until_exam;
    double score;
    std::string recommendation;
};

std::vector<ModuleStatus> compute_status(
    const std::vector<Module>& modules,
    const std::vector<WeekLog>& logs);

void show_status(const std::vector<ModuleStatus>& status);
