# Task 6 - Implement Symmetric Encryption

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-1-symmetric-encryption>

Short title: `Symmetric Encryption`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-2-1-symmetric-encryption dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-2-1-symmetric-encryption\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-2-1-symmetric-encryption\target\classes;.\track-26-securitor\task-24-2-1-symmetric-encryption\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
