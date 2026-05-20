#include "tracker.h"
#include <iostream>
#include <algorithm>

void Tracker::add_topic(const std::string& course, const std::string& name) {
    topics_.push_back({name, course});
    std::cout << "Topic added: [" << course << "] " << name << "\n";
}

void Tracker::log_session(const std::string& topic_name, int minutes) {
    for (auto& t : topics_) {
        if (t.name == topic_name) {
            t.study_minutes += minutes;
            std::cout << "Logged " << minutes << " min for: " << topic_name << "\n";
            return;
        }
    }
    std::cout << "Topic not found: " << topic_name << "\n";
}

std::vector<Topic*> Tracker::weak_topics(int threshold_minutes) {
    std::vector<Topic*> weak;
    for (auto& t : topics_) {
        if (t.study_minutes < threshold_minutes)
            weak.push_back(&t);
    }
    return weak;
}

void Tracker::show_overview() const {
    std::cout << "\n--- Semester Overview ---\n";
    for (const auto& t : topics_) {
        std::cout << "[" << t.course << "] " << t.name
                  << " - " << t.study_minutes << " min";
        if (t.study_minutes < 30) std::cout << " *** NEEDS ATTENTION";
        std::cout << "\n";
    }
    std::cout << "-------------------------\n\n";
}

void Tracker::suggest_questions() {
    auto weak = weak_topics();
    if (weak.empty()) {
        std::cout << "All topics look good!\n";
        return;
    }
    std::cout << "\n--- Review Questions for Weak Topics ---\n";
    for (auto* t : weak) {
        std::cout << "\n[" << t->course << "] " << t->name << " (" << t->study_minutes << " min studied):\n";
        if (!t->questions.empty()) {
            for (const auto& q : t->questions)
                std::cout << "  - " << q << "\n";
        } else {
            std::cout << "  - What are the key concepts of " << t->name << "?\n";
            std::cout << "  - Can you explain " << t->name << " in your own words?\n";
        }
    }
    std::cout << "----------------------------------------\n\n";
}
