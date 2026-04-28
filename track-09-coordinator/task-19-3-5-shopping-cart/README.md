# Task 15 - Implement E-Commerce Checkout Saga

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-5-shopping-cart>

Short title: `E-Commerce Saga`

Difficulty: `advanced`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-09-coordinator/task-19-3-5-shopping-cart dependency:copy-dependencies package
Get-Content .\track-09-coordinator\task-19-3-5-shopping-cart\samples\input.jsonl | java -cp '.\track-09-coordinator\task-19-3-5-shopping-cart\target\classes;.\track-09-coordinator\task-19-3-5-shopping-cart\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
