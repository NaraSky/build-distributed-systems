# Task 15 - Compare gRPC vs REST: Latency, Size, and DX

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-5-grpc-vs-rest>

Short title: `gRPC vs REST`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-3-5-grpc-vs-rest dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-3-5-grpc-vs-rest\samples\input.jsonl | java -cp '.\track-17-networker\task-5-3-5-grpc-vs-rest\target\classes;.\track-17-networker\task-5-3-5-grpc-vs-rest\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
