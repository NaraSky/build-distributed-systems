# Task 14 - Implement Consistent Hashing for Load Balancing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-4-consistent-hashing-lb>

Short title: `Consistent Hashing LB`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-3-4-consistent-hashing-lb dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-3-4-consistent-hashing-lb\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-3-4-consistent-hashing-lb\target\classes;.\track-14-loadbalancers\task-20-3-4-consistent-hashing-lb\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
