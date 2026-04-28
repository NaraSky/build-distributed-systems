# Task 14 - Implement Dotted Version Vectors

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-4-dotted-version-vectors>

Short title: `Dotted Version Vectors`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-3-4-dotted-version-vectors dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-3-4-dotted-version-vectors\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-3-4-dotted-version-vectors\target\classes;.\track-16-timekeeper\task-4-3-4-dotted-version-vectors\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
