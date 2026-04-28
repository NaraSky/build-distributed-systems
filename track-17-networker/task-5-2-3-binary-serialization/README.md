# Task 8 - Implement a Binary Serialization Format

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-3-binary-serialization>

Short title: `Binary Serialization`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-2-3-binary-serialization dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-2-3-binary-serialization\samples\input.jsonl | java -cp '.\track-17-networker\task-5-2-3-binary-serialization\target\classes;.\track-17-networker\task-5-2-3-binary-serialization\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
