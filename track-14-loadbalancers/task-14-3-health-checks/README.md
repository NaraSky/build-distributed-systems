# Task 3 - Add Health Checks and Failover

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-3-health-checks>

Short title: `Health Checks`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-14-3-health-checks dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-14-3-health-checks\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-14-3-health-checks\target\classes;.\track-14-loadbalancers\task-14-3-health-checks\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
