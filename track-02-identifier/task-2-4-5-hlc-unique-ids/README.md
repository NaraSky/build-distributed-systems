# Task 20 - HLC-Based Unique ID Generation for Maelstrom

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-5-hlc-unique-ids>

Short title: `HLC Unique IDs`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-4-5-hlc-unique-ids dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-4-5-hlc-unique-ids\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-4-5-hlc-unique-ids\target\classes;.\track-02-identifier\task-2-4-5-hlc-unique-ids\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
