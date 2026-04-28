# Task 7 - Implement Authentication and Authorization at Gateway

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-2-auth-gateway>

Short title: `Gateway Auth`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-12-proxies/task-21-2-2-auth-gateway dependency:copy-dependencies package
Get-Content .\track-12-proxies\task-21-2-2-auth-gateway\samples\input.jsonl | java -cp '.\track-12-proxies\task-21-2-2-auth-gateway\target\classes;.\track-12-proxies\task-21-2-2-auth-gateway\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
