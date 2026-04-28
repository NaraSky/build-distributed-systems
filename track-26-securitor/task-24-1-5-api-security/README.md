# Task 5 - Implement API Security Best Practices

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-5-api-security>

Short title: `API Security`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-1-5-api-security dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-1-5-api-security\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-1-5-api-security\target\classes;.\track-26-securitor\task-24-1-5-api-security\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
