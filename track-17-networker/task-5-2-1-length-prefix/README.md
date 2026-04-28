# Task 6 - Implement Length-Prefixed Message Framing

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-1-length-prefix>

Short title: `Length-Prefix Framing`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-2-1-length-prefix dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-2-1-length-prefix\samples\input.jsonl | java -cp '.\track-17-networker\task-5-2-1-length-prefix\target\classes;.\track-17-networker\task-5-2-1-length-prefix\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
