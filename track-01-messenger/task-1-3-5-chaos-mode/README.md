# Task 15 - Add Chaos Mode with Random Message Dropping

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-5-chaos-mode>

Short title: `Chaos Mode`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-01-messenger/task-1-3-5-chaos-mode dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-3-5-chaos-mode\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-3-5-chaos-mode\target\classes;.\track-01-messenger\task-1-3-5-chaos-mode\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
