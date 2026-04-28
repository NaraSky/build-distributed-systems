# Task 13 - Implement Vector Clocks

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-3-vector-clock>

Short title: `Vector Clock`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-3-3-vector-clock dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-3-3-vector-clock\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-3-3-vector-clock\target\classes;.\track-02-identifier\task-2-3-3-vector-clock\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
