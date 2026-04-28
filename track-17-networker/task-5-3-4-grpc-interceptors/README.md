# Task 14 - Build gRPC Interceptors for Logging, Auth, and Rate Limiting

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-4-grpc-interceptors>

Short title: `gRPC Interceptors`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-3-4-grpc-interceptors dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-3-4-grpc-interceptors\samples\input.jsonl | java -cp '.\track-17-networker\task-5-3-4-grpc-interceptors\target\classes;.\track-17-networker\task-5-3-4-grpc-interceptors\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
