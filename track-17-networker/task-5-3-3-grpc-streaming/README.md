# Task 13 - Implement gRPC Server and Bidirectional Streaming

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-3-grpc-streaming>

Short title: `gRPC Streaming`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-3-3-grpc-streaming dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-3-3-grpc-streaming\samples\input.jsonl | java -cp '.\track-17-networker\task-5-3-3-grpc-streaming\target\classes;.\track-17-networker\task-5-3-3-grpc-streaming\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
