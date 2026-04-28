# Task 10 - Implement Rate Limiting

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-5-rate-limiting>

Short title: `Rate Limiting`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-2-5-rate-limiting dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-2-5-rate-limiting\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-2-5-rate-limiting\target\classes;.\track-14-loadbalancers\task-20-2-5-rate-limiting\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
