# Task 2 - Implement Least Connections Algorithm

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-2-least-connections>

Short title: `Least Connections`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-14-2-least-connections dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-14-2-least-connections\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-14-2-least-connections\target\classes;.\track-14-loadbalancers\task-14-2-least-connections\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
