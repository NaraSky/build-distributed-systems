# Task 17 - Implement HLC Receive Rule

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-2-hlc-receive>

Short title: `HLC Receive`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-4-2-hlc-receive dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-4-2-hlc-receive\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-4-2-hlc-receive\target\classes;.\track-02-identifier\task-2-4-2-hlc-receive\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
