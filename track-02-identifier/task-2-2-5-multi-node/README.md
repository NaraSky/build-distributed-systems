# Task 10 - Multi-Node Snowflake ID Verification

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-5-multi-node>

Short title: `Multi-Node IDs`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-2-5-multi-node dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-2-5-multi-node\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-2-5-multi-node\target\classes;.\track-02-identifier\task-2-2-5-multi-node\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
