# Task 10 - Implement End-to-End Encryption (E2EE)

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-5-end-to-end-encryption>

Short title: `E2EE`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-2-5-end-to-end-encryption dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-2-5-end-to-end-encryption\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-2-5-end-to-end-encryption\target\classes;.\track-26-securitor\task-24-2-5-end-to-end-encryption\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
