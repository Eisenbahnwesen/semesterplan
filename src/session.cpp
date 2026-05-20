#include "tracker.h"
#include <iostream>
#include <string>

void run_interactive(Tracker& tracker) {
    std::string cmd;
    std::cout << "Semesterplan - Commands: add, log, overview, questions, quit\n\n";

    while (true) {
        std::cout << "> ";
        std::cin >> cmd;

        if (cmd == "add") {
            std::string course, topic;
            std::cout << "Course: "; std::cin >> course;
            std::cout << "Topic: "; std::cin >> topic;
            tracker.add_topic(course, topic);
        } else if (cmd == "log") {
            std::string topic;
            int minutes;
            std::cout << "Topic: "; std::cin >> topic;
            std::cout << "Minutes studied: "; std::cin >> minutes;
            tracker.log_session(topic, minutes);
        } else if (cmd == "overview") {
            tracker.show_overview();
        } else if (cmd == "questions") {
            tracker.suggest_questions();
        } else if (cmd == "quit") {
            break;
        } else {
            std::cout << "Unknown command\n";
        }
    }
}
