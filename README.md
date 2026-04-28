# Build Distributed Systems from Scratch

[English](#overview) | [中文](#项目简介)

> 348 道渐进式练习题，用 Java 从零构建分布式系统的核心组件。
>
> 348 progressive exercises to build core distributed systems components in Java from scratch.

## Overview

This project is a hands-on companion to [builddistributedsystem.com](https://builddistributedsystem.com/tracks). It contains **348 tasks** across **28 tracks**, covering the full spectrum of distributed systems — from basic message passing to Raft consensus, CRDT counters, distributed transactions, and more.

Every task runs on the [Maelstrom](https://github.com/jepsen-io/maelstrom) testing framework: your node reads JSON messages from stdin, processes them, and writes responses to stdout. No external infrastructure needed — just Java and Maven.

## 项目简介

本项目是 [builddistributedsystem.com](https://builddistributedsystem.com/tracks) 的本地 Java 练习仓库。包含 **28 个课程方向**、**348 道渐进式练习题**，从最基础的 JSON 消息解析，到 Raft 共识、CRDT、分布式事务等高级主题，循序渐进地构建分布式系统核心能力。

所有任务基于 [Maelstrom](https://github.com/jepsen-io/maelstrom) 测试框架：你的节点从标准输入读取 JSON 消息，处理后将响应写入标准输出。无需搭建外部基础设施，只需 Java 和 Maven 即可开始。

每道题都提供了**通俗易懂的中文题解**（`TASK.zh-CN.md`），适合初学者入门。

## Prerequisites

- **Java 21** or later
- **Maven 3.8+**

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/build-distributed-systems.git
cd build-distributed-systems

# Build the entire project
mvn compile

# Run all tests
mvn test
```

### Run a Single Task

```bash
# Build and package a specific task
mvn -q -pl track-01-messenger/task-1-1-json-parser dependency:copy-dependencies package

# Run it with sample input
cat track-01-messenger/task-1-1-json-parser/samples/input-1.jsonl | \
  java -cp 'track-01-messenger/task-1-1-json-parser/target/classes:track-01-messenger/task-1-1-json-parser/target/dependency/*' Main
```

### Build & Test a Single Track

```bash
mvn test -pl track-01-messenger
```

## Project Structure

```text
build-distributed-systems/
├── pom.xml                          # Root POM (Java 21, dependency management)
├── COURSE_MAP.md                    # Full course catalog with links
├── track-01-messenger/              # Track: messaging basics
│   ├── pom.xml                      # Track-level aggregator
│   ├── task-1-1-json-parser/        # Individual task module
│   │   ├── pom.xml
│   │   ├── TASK.md                  # Problem statement (English)
│   │   ├── TASK.zh-CN.md            # Problem statement (中文)
│   │   ├── NOTES.md                 # Personal notes template
│   │   ├── src/main/java/Main.java  # Your solution goes here
│   │   └── samples/                 # Sample input/expected output
│   │       ├── input-1.jsonl
│   │       └── expected-1.txt
│   └── task-1-2-init-handler/
│       └── ...
├── track-02-identifier/
│   └── ...
└── ...
```

**Key points:**
- Each task's solution is a single file: `src/main/java/Main.java`
- `TASK.md` / `TASK.zh-CN.md` — read these to understand the problem
- `samples/` — use these to test your solution locally
- `NOTES.md` — jot down your thoughts, debugging notes, and learnings

## Tracks Overview

| # | Track | Topic | Tasks |
|---|-------|-------|------:|
| 1 | [The Messenger](track-01-messenger/) | Message passing, RPC, protocol basics | 15 |
| 2 | [The Identifier](track-02-identifier/) | Distributed unique ID generation (Snowflake, UUID) | 19 |
| 3 | [The Gossiper](track-03-gossiper/) | Gossip protocols, epidemic broadcast | 19 |
| 4 | [The Counter](track-04-counter/) | Distributed counters, CRDTs | 15 |
| 5 | [The Elector](track-05-elector/) | Leader election algorithms | 5 |
| 6 | [The Consensus](track-06-consensus/) | Raft consensus, log replication | 20 |
| 7 | [The Store](track-07-store/) | Linearizable key-value store | 15 |
| 8 | [The Sharder](track-08-sharder/) | Sharding, data migration | 15 |
| 9 | [The Coordinator](track-09-coordinator/) | Distributed transactions (2PC) | 15 |
| 10 | [Advanced](track-10-advanced/) | Advanced distributed patterns | 5 |
| 11 | [Caches](track-11-caches/) | Distributed caching strategies | 5 |
| 12 | [Proxies](track-12-proxies/) | Reverse proxies, routing | 10 |
| 13 | [Indexes](track-13-indexes/) | Distributed indexing | 5 |
| 14 | [Load Balancers](track-14-loadbalancers/) | Load balancing algorithms | 15 |
| 15 | [Queues](track-15-queues/) | Distributed message queues | 10 |
| 16 | [The Timekeeper](track-16-timekeeper/) | Logical clocks (Lamport, Vector, HLC) | 20 |
| 17 | [The Networker](track-17-networker/) | TCP, protocol fundamentals | 15 |
| 19 | [The Logger](track-19-logger/) | WAL, LSM tree, distributed logs | 20 |
| 20 | [The Filesystem](track-20-filesystem/) | Distributed file storage | 10 |
| 22 | [The Watcher](track-22-watcher/) | ZooKeeper/etcd coordination model | 15 |
| 23 | [The Searcher](track-23-searcher/) | Distributed search | 10 |
| 24 | [The Scheduler](track-24-scheduler/) | Task scheduling | 10 |
| 25 | [The Tracer](track-25-tracer/) | Observability, distributed tracing | 10 |
| 26 | [The Securitor](track-26-securitor/) | Auth, encryption, security | 10 |
| 27 | [The Migrator](track-27-migrator/) | Data & protocol evolution | 10 |
| 28 | [The Orchestrator](track-28-orchestrator/) | Container orchestration, service mesh | 10 |
| 29 | [The Reactor](track-29-reactor/) | Event sourcing, CQRS | 10 |
| 30 | [The MapReducer](track-30-mapreducer/) | Batch & stream processing | 10 |

> Tracks 18 and 21 are embedded within tracks 08 (Sharder) and 12 (Proxies) on the website.

## How It Works

Each task follows the [Maelstrom protocol](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md):

```text
               stdin (JSON)              stdout (JSON)
  Maelstrom  ──────────────►  Your Node  ──────────────►  Maelstrom
              {"src":"c1",                {"src":"n1",
               "dest":"n1",               "dest":"c1",
               "body":{...}}              "body":{...}}
```

1. **Read** a JSON message from stdin (one per line)
2. **Process** the message according to the task requirements
3. **Write** a JSON response to stdout
4. **Debug** by writing to stderr (won't affect evaluation)

## Recommended Learning Path

If you're new to distributed systems, follow the tracks in order:

1. **The Messenger** — learn the basics of node communication
2. **The Identifier** — generate unique IDs without coordination
3. **The Gossiper** — spread information across a cluster
4. **The Counter** — manage distributed state with CRDTs
5. **The Elector** — elect a leader among nodes
6. **The Consensus** — implement Raft for agreement
7. **The Store** — build a linearizable key-value store
8. **The Coordinator** — handle distributed transactions

Then explore the remaining tracks based on your interests.

## Tech Stack

| Component | Version |
|-----------|---------|
| Java | 21 |
| Maven | 3.8+ |
| Jackson Databind | 2.17.2 |
| JUnit Jupiter | 5.10.3 |

## Contributing

Contributions are welcome! Some ways to contribute:

- Improve or add Chinese/English translations
- Fix errors in task descriptions
- Add more sample test cases
- Share your solution approaches (in a separate `solutions/` branch)

## Acknowledgments

- [Build Distributed Systems](https://builddistributedsystem.com) — the original course and task design
- [Maelstrom](https://github.com/jepsen-io/maelstrom) by Jepsen — the distributed systems testing framework
- [Designing Data-Intensive Applications](https://dataintensive.net/) by Martin Kleppmann — the book that inspired many of these concepts

## License

This project is for educational purposes. Task descriptions are derived from [builddistributedsystem.com](https://builddistributedsystem.com). Please refer to the original website for licensing terms.
