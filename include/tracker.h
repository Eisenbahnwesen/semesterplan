#pragma once
#include "topic.h"
#include <vector>
#include <string>

class Tracker {
public:
    void add_topic(const std::string& course, const std::string& name);
    void log_session(const std::string& topic_name, int minutes);
    std::vector<Topic*> weak_topics(int threshold_minutes = 30);
    void show_overview() const;
    void suggest_questions();

private:
    std::vector<Topic> topics_;
};
