# Task 11 - Define and Encode Protocol Buffer Messages

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-1-protobuf-schema>

Short title: `Protobuf Schema`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-3-1-protobuf-schema dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-3-1-protobuf-schema\samples\input.jsonl | java -cp '.\track-17-networker\task-5-3-1-protobuf-schema\target\classes;.\track-17-networker\task-5-3-1-protobuf-schema\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
