# Task 6 - Implement Layer 7 HTTP Proxy

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-1-http-proxy>

Short title: `HTTP Proxy`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-14-loadbalancers/task-20-2-1-http-proxy dependency:copy-dependencies package
Get-Content .\track-14-loadbalancers\task-20-2-1-http-proxy\samples\input.jsonl | java -cp '.\track-14-loadbalancers\task-20-2-1-http-proxy\target\classes;.\track-14-loadbalancers\task-20-2-1-http-proxy\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
