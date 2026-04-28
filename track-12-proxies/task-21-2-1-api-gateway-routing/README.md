# Task 6 - Implement API Gateway Service Routing

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-1-api-gateway-routing>

Short title: `API Gateway Routing`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-21-2-1-api-gateway-routing dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-21-2-1-api-gateway-routing\samples\input.jsonl | java -cp '.\track-12-proxies\task-21-2-1-api-gateway-routing\target\classes;.\track-12-proxies\task-21-2-1-api-gateway-routing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
