# 实现预写日志

英文标题：Implement a Write-Ahead Log
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-1-wal-impl>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：1
短标题：WAL Implementation
难度：进阶
子主题：提交日志（WAL）

## 中文导读

本题要求你实现一个预写日志（Write-Ahead Log），它是分布式系统中保证数据持久性的最基本组件。你需要实现追加写入、校验和验证以及磁盘同步三个核心能力。理解预写日志的工作原理，是深入学习数据库、共识算法和消息队列的基础。

## 题目说明

预写日志（Write-Ahead Log，简称 WAL）是分布式系统中最基础的持久化原语。所有数据库（PostgreSQL、MySQL、SQLite）、所有共识算法（Raft、Paxos）以及所有消息代理（Kafka）的核心都依赖 WAL。

其核心思想是：**在将变更应用到状态之前，先把变更写入日志**。这样，即使系统在任何时刻崩溃，都可以通过重放 WAL 来恢复到崩溃前的精确状态。

请实现一个具备以下特性的 WAL：
1. **仅追加写入**：条目一旦写入就不可修改，只能在末尾追加新条目
2. **校验和保护**：每个条目都包含一个 CRC32 校验和，用于检测数据损坏
3. **持久化保证**：条目在通过 fsync 刷盘之后，才向调用方返回确认

条目格式：`[4字节长度][4字节CRC32校验和][载荷字节]`

```json
Request:  {"type": "wal_append", "msg_id": 1, "payload": "set x=42"}
Response: {"type": "wal_append_ok", "in_reply_to": 1, "offset": 0, "length": 8, "checksum": "abc123"}

Request:  {"type": "wal_read", "msg_id": 2, "offset": 0}
Response: {"type": "wal_read_ok", "in_reply_to": 2, "payload": "set x=42", "checksum_valid": true}

Request:  {"type": "wal_info", "msg_id": 3}
Response: {"type": "wal_info_ok", "in_reply_to": 3, "entries": 1, "total_bytes": 16, "fsynced": true}
```

## 涉及概念

- `write-ahead log`
- `append-only`
- `checksum`
- `durability`
- `fsync`

## 实现提示

- 每个条目的格式为：[4字节长度][4字节CRC32校验和][载荷字节]
- 必须先写入磁盘并调用 fsync，然后再向调用方返回确认，这就是"预写"保证的含义
- 校验和用于检测不完整写入：如果写入过程中发生崩溃，部分写入的条目将具有无效的校验和
- 使用 CRC32 作为校验和算法，它速度快，且足以检测数据损坏
- WAL 是仅追加写入的：永远不要修改已有条目，只在末尾添加新条目

## 测试用例

### 1. 追加单条记录并读取

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"set x=42"}}
{"src":"c1","dest":"n1","body":{"type":"wal_read","msg_id":3,"offset":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_read_ok", "in_reply_to": 3, "payload": "set x=42", "checksum_valid": true, "msg_id": 2}}
```

### 2. 多次追加后偏移量递增

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"op1"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":3,"payload":"op2"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":4,"payload":"op3"}}
{"src":"c1","dest":"n1","body":{"type":"wal_info","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 3, "offset": 1, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 4, "offset": 2, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_info_ok", "in_reply_to": 5, "entries": 3, "msg_id": 4}}
```

## 参考资料

- [Write-Ahead Logging - PostgreSQL](https://www.postgresql.org/docs/current/wal-intro.html)：PostgreSQL 官方文档，介绍预写日志的基本原理

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
