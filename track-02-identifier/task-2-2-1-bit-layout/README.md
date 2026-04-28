# Task 6 - Implement Snowflake ID Bit Layout

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-1-bit-layout>

Short title: `Bit Layout`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-2-1-bit-layout dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-2-1-bit-layout\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-2-1-bit-layout\target\classes;.\track-02-identifier\task-2-2-1-bit-layout\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
