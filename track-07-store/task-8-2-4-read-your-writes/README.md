# Task 9 - Guarantee Read-Your-Writes with Follower Reads

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-4-read-your-writes>

Short title: `Read-Your-Writes`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-2-4-read-your-writes dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-2-4-read-your-writes\samples\input.jsonl | java -cp '.\track-07-store\task-8-2-4-read-your-writes\target\classes;.\track-07-store\task-8-2-4-read-your-writes\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
