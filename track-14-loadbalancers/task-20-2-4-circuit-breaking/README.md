# Task 9 - Implement Circuit Breaking

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-4-circuit-breaking>

Short title: `Circuit Breaking`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-2-4-circuit-breaking dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-2-4-circuit-breaking\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-2-4-circuit-breaking\target\classes;.\track-14-loadbalancers\task-20-2-4-circuit-breaking\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
