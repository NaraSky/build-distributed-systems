# Task 14 - Implement Happened-Before Detector with Vector Clocks

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-4-happened-before>

Short title: `Happened-Before`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-3-4-happened-before dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-3-4-happened-before\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-3-4-happened-before\target\classes;.\track-02-identifier\task-2-3-4-happened-before\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
