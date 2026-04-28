# Task 15 - Simulate Thundering Herd with Circuit Breaking

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-5-thundering-herd>

Short title: `Thundering Herd`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-3-5-thundering-herd dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-3-5-thundering-herd\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-3-5-thundering-herd\target\classes;.\track-14-loadbalancers\task-20-3-5-thundering-herd\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
