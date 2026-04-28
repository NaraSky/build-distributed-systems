# Task 2 - Add Random Salt to Prevent Collisions

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-random-salt>

Short title: `Random Salt`

Difficulty: `beginner`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-2-random-salt dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-2-random-salt\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-2-random-salt\target\classes;.\track-02-identifier\task-2-2-random-salt\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
