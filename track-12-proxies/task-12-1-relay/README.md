# Task 1 - Implement Basic Relay Proxy

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-1-relay>

Short title: `Relay Proxy`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-12-1-relay dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-12-1-relay\samples\input.jsonl | java -cp '.\track-12-proxies\task-12-1-relay\target\classes;.\track-12-proxies\task-12-1-relay\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
