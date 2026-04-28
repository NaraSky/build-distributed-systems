# Build Distributed Systems from Scratch - Java 21

This repository maps <https://builddistributedsystem.com/tracks> to local Java 21 Maven modules.

Each website track is a Maven aggregator module. Each website task is a Maven child module with the Java starter code in:

```text
src/main/java/Main.java
```

Each task module also contains the corresponding problem statement in:

```text
TASK.md
```

The local Maven files are for editing, dependency management, and local verification. For website submission, use the task module's `Main.java`.

## Generated Course Map

| Track | Local module | Website title | Tasks generated/site count |
| --- | --- | --- | --- |
| 1 | `track-01-messenger` | The Messenger | 15/15 |
| 2 | `track-02-identifier` | The Identifier | 19/19 |
| 3 | `track-03-gossiper` | The Gossiper | 19/19 |
| 4 | `track-04-counter` | The Counter | 15/15 |
| 5 | `track-05-elector` | The Elector | 5/5 |
| 6 | `track-06-consensus` | The Consensus | 20/20 |
| 7 | `track-07-store` | The Store | 15/15 |
| 8 | `track-08-sharder` | The Sharder | 15/15 |
| 9 | `track-09-coordinator` | The Coordinator | 15/15 |
| 10 | `track-10-advanced` | Advanced | 5/5 |
| 11 | `track-11-caches` | Caches | 5/5 |
| 12 | `track-12-proxies` | Proxies | 10/10 |
| 13 | `track-13-indexes` | Indexes | 5/5 |
| 14 | `track-14-loadbalancers` | Load Balancers | 15/15 |
| 15 | `track-15-queues` | Queues | 10/10 |
| 16 | `track-16-timekeeper` | The Timekeeper | 20/20 |
| 17 | `track-17-networker` | The Networker | 15/15 |
| 19 | `track-19-logger` | The Logger | 20/20 |
| 20 | `track-20-filesystem` | The Filesystem | 10/10 |
| 22 | `track-22-watcher` | The Watcher | 15/15 |
| 23 | `track-23-searcher` | The Searcher | 10/10 |
| 24 | `track-24-scheduler` | The Scheduler | 10/10 |
| 25 | `track-25-tracer` | The Tracer | 10/10 |
| 26 | `track-26-securitor` | The Securitor | 10/10 |
| 27 | `track-27-migrator` | The Migrator | 10/10 |
| 28 | `track-28-orchestrator` | The Orchestrator | 10/10 |
| 29 | `track-29-reactor` | The Reactor | 10/10 |
| 30 | `track-30-mapreducer` | The MapReducer | 10/10 |

Total generated task modules: `348`.

## Build

```powershell
cd D:\code\build-distributed-systems-java
mvn test
```

## Run One Task Locally

Example:

```powershell
mvn -q -pl track-01-messenger/task-1-1-json-parser dependency:copy-dependencies package
Get-Content .\track-01-messenger\task-1-1-json-parser\samples\input.jsonl | java -cp '.\track-01-messenger\task-1-1-json-parser\target\classes;.\track-01-messenger\task-1-1-json-parser\target\dependency\*' Main
```

## Notes

The Java starter code is copied from the website API field `starterCodeJava` when the API allowed access. Some tasks provide a generic Java template rather than a task-specific Java implementation; that is the website's current Java starter state.
