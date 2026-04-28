# Task 13 - Implement Power-of-Two-Choices Load Balancing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-3-power-of-two-choices>

Short title: `Power-of-Two-Choices`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-3-3-power-of-two-choices dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-3-3-power-of-two-choices\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-3-3-power-of-two-choices\target\classes;.\track-14-loadbalancers\task-20-3-3-power-of-two-choices\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
