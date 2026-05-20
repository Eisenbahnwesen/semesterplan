#pragma once
#include "module.h"
#include <string>
#include <vector>

bool load_data(const std::string& path,
               std::vector<Module>& modules,
               std::vector<WeekLog>& logs);

void save_data(const std::string& path,
               const std::vector<Module>& modules,
               const std::vector<WeekLog>& logs);
