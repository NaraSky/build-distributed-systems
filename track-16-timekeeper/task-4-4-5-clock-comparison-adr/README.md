# Task 20 - Architecture Decision Record: Choosing a Clock System

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-5-clock-comparison-adr>

Short title: `Clock ADR`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-4-5-clock-comparison-adr dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-4-5-clock-comparison-adr\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-4-5-clock-comparison-adr\target\classes;.\track-16-timekeeper\task-4-4-5-clock-comparison-adr\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
