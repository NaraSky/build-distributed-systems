# Task 3 - Implement Collapsed Forwarding

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-3-collapsed>

Short title: `Collapsed Forwarding`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-12-3-collapsed dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-12-3-collapsed\samples\input.jsonl | java -cp '.\track-12-proxies\task-12-3-collapsed\target\classes;.\track-12-proxies\task-12-3-collapsed\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
