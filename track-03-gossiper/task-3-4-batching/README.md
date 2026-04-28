# Task 4 - Add Message Batching to Reduce Network Overhead

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-batching>

Short title: `Message Batching`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-03-gossiper/task-3-4-batching dependency:copy-dependencies package
Get-Content .\track-03-gossiper\task-3-4-batching\samples\input.jsonl | java -cp '.\track-03-gossiper\task-3-4-batching\target\classes;.\track-03-gossiper\task-3-4-batching\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
