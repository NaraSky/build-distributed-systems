# Task 5 - Implement Resource Estimation and Provisioning

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-5-resource-estimation>

Short title: `Resource Estimation`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-24-scheduler/task-22-1-5-resource-estimation dependency:copy-dependencies package
Get-Content .\track-24-scheduler\task-22-1-5-resource-estimation\samples\input.jsonl | java -cp '.\track-24-scheduler\task-22-1-5-resource-estimation\target\classes;.\track-24-scheduler\task-22-1-5-resource-estimation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
