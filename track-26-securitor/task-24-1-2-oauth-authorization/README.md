# Task 2 - Implement OAuth 2.0 Authorization Flow

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-2-oauth-authorization>

Short title: `OAuth 2.0`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-1-2-oauth-authorization dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-1-2-oauth-authorization\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-1-2-oauth-authorization\target\classes;.\track-26-securitor\task-24-1-2-oauth-authorization\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
