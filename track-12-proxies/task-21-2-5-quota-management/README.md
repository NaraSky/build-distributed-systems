# Task 10 - Implement Rate Limiting and Quota Management

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-5-quota-management>

Short title: `Rate Limiting and Quotas`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-21-2-5-quota-management dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-21-2-5-quota-management\samples\input.jsonl | java -cp '.\track-12-proxies\task-21-2-5-quota-management\target\classes;.\track-12-proxies\task-21-2-5-quota-management\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
