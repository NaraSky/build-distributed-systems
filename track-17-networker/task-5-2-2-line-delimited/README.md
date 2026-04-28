# Task 7 - Implement Line-Delimited Framing (Redis RESP Style)

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-2-line-delimited>

Short title: `Line-Delimited Framing`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-2-2-line-delimited dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-2-2-line-delimited\samples\input.jsonl | java -cp '.\track-17-networker\task-5-2-2-line-delimited\target\classes;.\track-17-networker\task-5-2-2-line-delimited\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
