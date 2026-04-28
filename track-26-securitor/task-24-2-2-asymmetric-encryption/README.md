# Task 7 - Implement Asymmetric Encryption (RSA)

Website: <https://builddistributedsystem.com/tracks/securitor/tasks/task-24-2-2-asymmetric-encryption>

Short title: `Asymmetric Encryption`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-26-securitor/task-24-2-2-asymmetric-encryption dependency:copy-dependencies package
Get-Content .\track-26-securitor\task-24-2-2-asymmetric-encryption\samples\input.jsonl | java -cp '.\track-26-securitor\task-24-2-2-asymmetric-encryption\target\classes;.\track-26-securitor\task-24-2-2-asymmetric-encryption\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
