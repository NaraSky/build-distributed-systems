# Task 3 - Implement Compare-And-Swap (CAS) Operation

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-3-cas-operation>

Short title: `Compare-And-Swap`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-4-3-cas-operation dependency:copy-dependencies package
Get-Content .\track-04-counter\task-4-3-cas-operation\samples\input.jsonl | java -cp '.\track-04-counter\task-4-3-cas-operation\target\classes;.\track-04-counter\task-4-3-cas-operation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
