# Task 10 - Implement Dynamic Scheduling with Locality Awareness

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-5-dynamic-scheduling>

Short title: `Locality Scheduling`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-2-5-dynamic-scheduling dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-2-5-dynamic-scheduling\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-2-5-dynamic-scheduling\target\classes;.\track-24-scheduler\task-22-2-5-dynamic-scheduling\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
