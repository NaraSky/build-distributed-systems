# Task 7 - Implement Path-Based Routing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-2-path-routing>

Short title: `Path-Based Routing`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-2-2-path-routing dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-2-2-path-routing\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-2-2-path-routing\target\classes;.\track-14-loadbalancers\task-20-2-2-path-routing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
