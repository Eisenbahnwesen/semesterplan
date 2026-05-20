# Semesterplan

A C++ CLI tool that tracks your lecture topics and automatically generates targeted review questions for topics you haven't studied enough.

## Features
- Track topics per course/module
- Log study sessions
- Detect under-studied topics
- Generate review questions for weak areas

## Project Structure
```
semesterplan/
├── src/          # Source files
├── include/      # Header files
├── data/         # Topic & session data (JSON)
└── CMakeLists.txt
```

## Build
```bash
mkdir build && cd build
cmake ..
make
```
