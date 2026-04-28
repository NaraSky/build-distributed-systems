# Task 13 - Build a Causal-Order Chat System

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-3-causal-chat>

Short title: `Causal Chat`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-16-timekeeper/task-4-3-3-causal-chat dependency:copy-dependencies package
Get-Content .\track-16-timekeeper\task-4-3-3-causal-chat\samples\input.jsonl | java -cp '.\track-16-timekeeper\task-4-3-3-causal-chat\target\classes;.\track-16-timekeeper\task-4-3-3-causal-chat\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
