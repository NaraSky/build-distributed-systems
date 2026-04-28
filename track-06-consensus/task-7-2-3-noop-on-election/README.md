# Task 8 - Handle Leader Changes with No-Op on Election

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-3-noop-on-election>

Short title: `No-Op on Election`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-06-consensus/task-7-2-3-noop-on-election dependency:copy-dependencies package
Get-Content .\track-06-consensus\task-7-2-3-noop-on-election\samples\input.jsonl | java -cp '.\track-06-consensus\task-7-2-3-noop-on-election\target\classes;.\track-06-consensus\task-7-2-3-noop-on-election\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
