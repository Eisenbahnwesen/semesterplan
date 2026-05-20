cmake_minimum_required(VERSION 3.15)
project(semesterplan VERSION 0.2.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(json
    URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz
)
FetchContent_MakeAvailable(json)

include_directories(include)

add_executable(semesterplan
    src/main.cpp
    src/onboarding.cpp
    src/checkin.cpp
    src/planner.cpp
    src/storage.cpp
)

target_link_libraries(semesterplan PRIVATE nlohmann_json::nlohmann_json)
