# Task 12 - Implement a gRPC Unary RPC Service

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-2-grpc-unary>

Short title: `gRPC Unary`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-3-2-grpc-unary dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-3-2-grpc-unary\samples\input.jsonl | java -cp '.\track-17-networker\task-5-3-2-grpc-unary\target\classes;.\track-17-networker\task-5-3-2-grpc-unary\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
