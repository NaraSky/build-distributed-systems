# Task 8 - Implement Query Side Optimization

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-3-query-side>

Short title: `Query Side`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-29-reactor/task-27-2-3-query-side dependency:copy-dependencies package
Get-Content .\track-29-reactor\task-27-2-3-query-side\samples\input.jsonl | java -cp '.\track-29-reactor\task-27-2-3-query-side\target\classes;.\track-29-reactor\task-27-2-3-query-side\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
