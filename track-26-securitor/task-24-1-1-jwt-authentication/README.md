# Task 1 - Implement JWT Authentication System

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-1-jwt-authentication>

Short title: `JWT Auth`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-1-1-jwt-authentication dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-1-1-jwt-authentication\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-1-1-jwt-authentication\target\classes;.\track-26-securitor\task-24-1-1-jwt-authentication\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
