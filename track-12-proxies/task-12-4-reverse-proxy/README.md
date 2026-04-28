# Task 4 - Build Reverse Proxy with Caching

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-4-reverse-proxy>

Short title: `Reverse Proxy`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-12-4-reverse-proxy dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-12-4-reverse-proxy\samples\input.jsonl | java -cp '.\track-12-proxies\task-12-4-reverse-proxy\target\classes;.\track-12-proxies\task-12-4-reverse-proxy\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
