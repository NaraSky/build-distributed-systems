# Task 8 - Add Follower Reads with Bounded Staleness

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-3-follower-reads>

Short title: `Follower Reads`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-07-store/task-8-2-3-follower-reads dependency:copy-dependencies package
Get-Content .\track-07-store\task-8-2-3-follower-reads\samples\input.jsonl | java -cp '.\track-07-store\task-8-2-3-follower-reads\target\classes;.\track-07-store\task-8-2-3-follower-reads\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
