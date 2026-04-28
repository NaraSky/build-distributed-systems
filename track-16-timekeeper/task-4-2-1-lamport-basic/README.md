# Task 6 - Implement a Lamport Clock from Scratch

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-1-lamport-basic>

Short title: `Lamport Basic`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-2-1-lamport-basic dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-2-1-lamport-basic\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-2-1-lamport-basic\target\classes;.\track-16-timekeeper\task-4-2-1-lamport-basic\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
