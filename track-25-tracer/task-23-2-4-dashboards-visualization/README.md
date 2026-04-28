# Task 9 - Implement Monitoring Dashboards and Visualization

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-4-dashboards-visualization>

Short title: `Dashboards`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-25-tracer/task-23-2-4-dashboards-visualization dependency:copy-dependencies package
Get-Content .\track-25-tracer\task-23-2-4-dashboards-visualization\samples\input.jsonl | java -cp '.\track-25-tracer\task-23-2-4-dashboards-visualization\target\classes;.\track-25-tracer\task-23-2-4-dashboards-visualization\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
