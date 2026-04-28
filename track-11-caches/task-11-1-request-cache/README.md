# Task 1 - Implement Request Node Cache

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-1-request-cache>

Short title: `Request Cache`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-11-caches/task-11-1-request-cache dependency:copy-dependencies package
Get-Content .\track-11-caches\task-11-1-request-cache\samples\input.jsonl | java -cp '.\track-11-caches\task-11-1-request-cache\target\classes;.\track-11-caches\task-11-1-request-cache\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
