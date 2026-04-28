# Task 10 - Implement Rendezvous Hashing (Highest Random Weight)

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-5-rendezvous-hashing>

Short title: `Rendezvous Hashing`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-08-sharder/task-18-2-5-rendezvous-hashing dependency:copy-dependencies package
Get-Content .\track-08-sharder\task-18-2-5-rendezvous-hashing\samples\input.jsonl | java -cp '.\track-08-sharder\task-18-2-5-rendezvous-hashing\target\classes;.\track-08-sharder\task-18-2-5-rendezvous-hashing\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
