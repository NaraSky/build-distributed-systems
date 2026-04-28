# Task 8 - Implement Cryptographic Hash Functions

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-3-hash-functions>

Short title: `Hash Functions`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-2-3-hash-functions dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-2-3-hash-functions\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-2-3-hash-functions\target\classes;.\track-26-securitor\task-24-2-3-hash-functions\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
