# Task 2 - Build Distributed Hash Table (Chord)

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-2-dht>

Short title: `DHT`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-10-advanced/task-10-2-dht dependency:copy-dependencies package
Get-Content .\track-10-advanced\task-10-2-dht\samples\input.jsonl | java -cp '.\track-10-advanced\task-10-2-dht\target\classes;.\track-10-advanced\task-10-2-dht\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
