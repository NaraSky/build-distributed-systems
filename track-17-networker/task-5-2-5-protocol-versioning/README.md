# Task 10 - Implement Protocol Versioning with Backward Compatibility

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-5-protocol-versioning>

Short title: `Protocol Versioning`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-2-5-protocol-versioning dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-2-5-protocol-versioning\samples\input.jsonl | java -cp '.\track-17-networker\task-5-2-5-protocol-versioning\target\classes;.\track-17-networker\task-5-2-5-protocol-versioning\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
