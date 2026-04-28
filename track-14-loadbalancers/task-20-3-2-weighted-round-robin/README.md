# Task 12 - Implement Weighted Round-Robin Load Balancing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-2-weighted-round-robin>

Short title: `Weighted Round-Robin`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-3-2-weighted-round-robin dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-3-2-weighted-round-robin\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-3-2-weighted-round-robin\target\classes;.\track-14-loadbalancers\task-20-3-2-weighted-round-robin\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
