# Task 3 - Implement a Text Analysis Pipeline

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-3-text-analysis>

Short title: `Text Analysis`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-23-searcher/task-16-1-3-text-analysis dependency:copy-dependencies package
Get-Content .\track-23-searcher\task-16-1-3-text-analysis\samples\input.jsonl | java -cp '.\track-23-searcher\task-16-1-3-text-analysis\target\classes;.\track-23-searcher\task-16-1-3-text-analysis\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
