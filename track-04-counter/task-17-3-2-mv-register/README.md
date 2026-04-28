# Task 12 - Implement a Multi-Value Register (MV-Register)

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-2-mv-register>

Short title: `MV-Register`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-3-2-mv-register dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-3-2-mv-register\samples\input.jsonl | java -cp '.\track-04-counter\task-17-3-2-mv-register\target\classes;.\track-04-counter\task-17-3-2-mv-register\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
