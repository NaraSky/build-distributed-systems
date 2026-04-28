# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Java 21 course project mapping [builddistributedsystem.com](https://builddistributedsystem.com/tracks) to local Maven modules. 348 tasks across 28 tracks cover distributed systems topics (messaging, consensus, sharding, CRDTs, etc.) using the Maelstrom testing framework.

## Build & Test

```bash
# Build and test everything
mvn test

# Build and test a single track
mvn test -pl track-01-messenger

# Build and test a single task
mvn test -pl track-01-messenger/task-1-1-json-parser

# Package a task and run it with sample input (macOS/Linux)
mvn -q -pl track-01-messenger/task-1-1-json-parser dependency:copy-dependencies package
cat track-01-messenger/task-1-1-json-parser/samples/input.jsonl | java -cp 'track-01-messenger/task-1-1-json-parser/target/classes:track-01-messenger/task-1-1-json-parser/target/dependency/*' Main
```

## Module Hierarchy

Three-level Maven aggregator structure:
- **Root pom.xml** — parent POM with Java 21, Jackson 2.17.2, JUnit 5.10.3 dependency management
- **`track-NN-name/pom.xml`** — track-level aggregator (packaging=pom), lists task modules
- **`track-NN-name/task-X-Y-slug/pom.xml`** — leaf module with actual code

Each task module's implementation lives in a single file: `src/main/java/Main.java`. This is the file to edit when solving a task, and the file submitted to the website.

## Task Documentation

Each task directory contains:
- `TASK.md` — English problem statement, test cases, hints
- `TASK.zh-CN.md` — Chinese translation with additional study notes
- `NOTES.md` — personal notes template (understanding, protocol, debugging)
- `samples/` — input/expected-output files (`input-N.jsonl`, `expected-N.txt`)
- `run.ps1` — PowerShell runner script (Windows-oriented)

## Maelstrom Protocol

Tasks use the Maelstrom protocol: JSON messages over stdin/stdout, one per line. Every message has `src`, `dest`, and `body` (with `type` field). Nodes read from stdin and write responses to stdout. Use stderr for debug logging.

## Code Generation Scripts

`scripts/generate_course_docs.py` fetches task metadata from the website API and generates TASK.zh-CN.md, samples, NOTES.md templates, and COURSE_MAP.md. Do not manually edit generated files.

## Key Dependencies

- Jackson Databind (JSON parsing) — available to all task modules via parent POM
- JUnit Jupiter 5 (testing) — test scope
