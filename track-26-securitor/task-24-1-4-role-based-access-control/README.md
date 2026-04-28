# Task 4 - Implement Role-Based Access Control (RBAC)

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-4-role-based-access-control>

Short title: `RBAC`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-1-4-role-based-access-control dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-1-4-role-based-access-control\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-1-4-role-based-access-control\target\classes;.\track-26-securitor\task-24-1-4-role-based-access-control\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
