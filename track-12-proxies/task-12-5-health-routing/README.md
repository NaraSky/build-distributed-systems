# Task 5 - Add Health-Based Routing

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-5-health-routing>

Short title: `Health Routing`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-12-5-health-routing dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-12-5-health-routing\samples\input.jsonl | java -cp '.\track-12-proxies\task-12-5-health-routing\target\classes;.\track-12-proxies\task-12-5-health-routing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
