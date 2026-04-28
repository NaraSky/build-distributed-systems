# Task 4 - Validate Uniqueness Across Distributed Nodes

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-uniqueness-validation>

Short title: `Uniqueness Validation`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-02-identifier/task-2-4-uniqueness-validation dependency:copy-dependencies package
Get-Content .\track-02-identifier\task-2-4-uniqueness-validation\samples\input.jsonl | java -cp '.\track-02-identifier\task-2-4-uniqueness-validation\target\classes;.\track-02-identifier\task-2-4-uniqueness-validation\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
