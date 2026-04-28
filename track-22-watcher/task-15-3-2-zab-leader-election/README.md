# Task 12 - Implement ZAB Leader Election with FastLeaderElection

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-2-zab-leader-election>

Short title: `ZAB Election`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-22-watcher/task-15-3-2-zab-leader-election dependency:copy-dependencies package
Get-Content .\track-22-watcher\task-15-3-2-zab-leader-election\samples\input.jsonl | java -cp '.\track-22-watcher\task-15-3-2-zab-leader-election\target\classes;.\track-22-watcher\task-15-3-2-zab-leader-election\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
