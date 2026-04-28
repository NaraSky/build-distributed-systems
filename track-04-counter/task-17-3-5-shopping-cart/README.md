# Task 15 - Build a Distributed Shopping Cart with CRDTs

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-5-shopping-cart>

Short title: `CRDT Shopping Cart`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-04-counter/task-17-3-5-shopping-cart dependency:copy-dependencies package
Get-Content .\track-04-counter\task-17-3-5-shopping-cart\samples\input.jsonl | java -cp '.\track-04-counter\task-17-3-5-shopping-cart\target\classes;.\track-04-counter\task-17-3-5-shopping-cart\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
