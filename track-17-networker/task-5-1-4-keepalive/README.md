# Task 4 - Implement Application-Level TCP Keep-Alive

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-4-keepalive>

Short title: `TCP Keep-Alive`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-1-4-keepalive dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-1-4-keepalive\samples\input.jsonl | java -cp '.\track-17-networker\task-5-1-4-keepalive\target\classes;.\track-17-networker\task-5-1-4-keepalive\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
