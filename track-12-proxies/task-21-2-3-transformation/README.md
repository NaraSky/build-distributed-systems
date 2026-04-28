# Task 8 - Implement Request/Response Transformation

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-3-transformation>

Short title: `Request/Response Transformation`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-21-2-3-transformation dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-21-2-3-transformation\samples\input.jsonl | java -cp '.\track-12-proxies\task-21-2-3-transformation\target\classes;.\track-12-proxies\task-21-2-3-transformation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
