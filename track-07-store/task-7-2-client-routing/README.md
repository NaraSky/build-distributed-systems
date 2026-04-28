# Task 2 - Handle Client Request Routing

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-2-client-routing>

Short title: `Client Routing`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-7-2-client-routing dependency:copy-dependencies package
Get-Content .\track-07-store\task-7-2-client-routing\samples\input.jsonl | java -cp '.\track-07-store\task-7-2-client-routing\target\classes;.\track-07-store\task-7-2-client-routing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
