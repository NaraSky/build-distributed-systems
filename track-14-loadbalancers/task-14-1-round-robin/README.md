# Task 1 - Implement Round Robin Load Balancer

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-1-round-robin>

Short title: `Round Robin`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-14-1-round-robin dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-14-1-round-robin\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-14-1-round-robin\target\classes;.\track-14-loadbalancers\task-14-1-round-robin\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
