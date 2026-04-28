# Task 8 - Implement Sticky Sessions

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-3-sticky-sessions>

Short title: `Sticky Sessions`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-2-3-sticky-sessions dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-2-3-sticky-sessions\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-2-3-sticky-sessions\target\classes;.\track-14-loadbalancers\task-20-2-3-sticky-sessions\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
