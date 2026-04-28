# Task 7 - Implement Command Side Validation and Execution

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-2-command-side>

Short title: `Command Side`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-2-2-command-side dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-2-2-command-side\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-2-2-command-side\target\classes;.\track-29-reactor\task-27-2-2-command-side\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
