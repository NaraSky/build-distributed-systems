# Task 5 - Optimize for High-Throughput ID Generation

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-5-high-throughput>

Short title: `High Throughput`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-5-high-throughput dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-5-high-throughput\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-5-high-throughput\target\classes;.\track-02-identifier\task-2-5-high-throughput\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
