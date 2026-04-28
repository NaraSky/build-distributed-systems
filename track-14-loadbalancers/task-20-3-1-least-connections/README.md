# Task 11 - Implement Least-Connections Load Balancing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-1-least-connections>

Short title: `Least-Connections`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-3-1-least-connections dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-3-1-least-connections\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-3-1-least-connections\target\classes;.\track-14-loadbalancers\task-20-3-1-least-connections\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
