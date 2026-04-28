# Task 4 - Build Layer 7 Load Balancer

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-4-layer7>

Short title: `Layer 7 LB`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-14-4-layer7 dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-14-4-layer7\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-14-4-layer7\target\classes;.\track-14-loadbalancers\task-14-4-layer7\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
