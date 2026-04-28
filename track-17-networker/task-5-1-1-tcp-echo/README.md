# Task 1 - Build a TCP Echo Server from Raw Syscalls

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-1-tcp-echo>

Short title: `TCP Echo Server`

Difficulty: `intermediate`

Local entry point:

```text
src/main/java/Main.java
```

Run locally from repo root:

```powershell
mvn -q -pl track-17-networker/task-5-1-1-tcp-echo dependency:copy-dependencies package
Get-Content .\track-17-networker\task-5-1-1-tcp-echo\samples\input.jsonl | java -cp '.\track-17-networker\task-5-1-1-tcp-echo\target\classes;.\track-17-networker\task-5-1-1-tcp-echo\target\dependency\*' Main
```

Submit the contents of `src/main/java/Main.java` to the website.
