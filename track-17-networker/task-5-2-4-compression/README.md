# Task 9 - Add Message Compression with CPU-Bandwidth Tradeoff Analysis

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-4-compression>

Short title: `Compression Tradeoff`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-2-4-compression dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-2-4-compression\samples\input.jsonl | java -cp '.\track-17-networker\task-5-2-4-compression\target\classes;.\track-17-networker\task-5-2-4-compression\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
