# 实现 WAL Recovery on Startup

英文标题：Implement WAL Recovery on Startup
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-2-wal-recovery>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：2
短标题：WAL Recovery
难度：intermediate
子主题：The Commit 日志 (WAL)

## 中文导读

本题要求你完成 `实现 WAL Recovery on Startup`。

重点关注：`crash recovery`、`log replay`、`checksum validation`、`torn writes`、`state reconstruction`。

建议先按提示逐步实现：On startup, scan the WAL sequentially from the beginning。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

WAL recovery is the other half of the durability story. When a 节点 restarts after a crash, it must scan the WAL和replay all valid entries to reconstruct its state.

The recovery algorithm:
1. Open the WAL file和read entries sequentially
2. For each entry, validate the checksum (recompute CRC32和compare)
3. If the checksum matches, replay the entry (apply the operation to the state machine)
4. If the checksum is invalid, this is a **torn write** — the entry was partially written before the crash. Skip it和all subsequent entries.
5. After replay, the state machine reflects the last consistent state

This is how every database recovers from crashes: PostgreSQL replays its WAL, SQLite replays its journal,和Raft replays its 日志.

```JSON
请求:  {"type": "wal_recover", "msg_id": 1, "wal_entries": [
    {"offset": 0, "payload": "set x=1", "checksum": "valid"},
    {"offset": 1, "payload": "set y=2", "checksum": "valid"},
    {"offset": 2, "payload": "set z=", "checksum": "invalid"}
]}
响应: {"type": "wal_recover_ok", "in_reply_to": 1, "entries_replayed": 2, "entries_skipped": 1, "state": {"x": "1", "y": "2"}}
```

## 涉及概念

- `crash recovery`
- `log replay`
- `checksum validation`
- `torn writes`
- `state reconstruction`

## 实现提示

- On startup, scan the WAL sequentially from the beginning
- For each entry, recompute the CRC32 checksum和compare to the stored one
- Valid entries are replayed to reconstruct state; invalid entries are skipped
- A torn write (crash mid-write) produces a partial entry，包含an invalid checksum
- After recovery, the state machine is identical to the last consistent pre-crash state

## 测试用例

### 1. Recovery replays valid entries和skips corrupted

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_recover","msg_id":2,"wal_entries":[{"offset":0,"payload":"set x=1","checksum":"valid"},{"offset":1,"payload":"set y=2","checksum":"valid"},{"offset":2,"payload":"set z=","checksum":"invalid"}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_recover_ok", "in_reply_to": 2, "entries_replayed": 2, "entries_skipped": 1, "msg_id": 1}}
```

### 2. Recovery，包含all valid entries replays everything

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_recover","msg_id":2,"wal_entries":[{"offset":0,"payload":"set a=10","checksum":"valid"},{"offset":1,"payload":"set b=20","checksum":"valid"},{"offset":2,"payload":"set c=30","checksum":"valid"}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_recover_ok", "in_reply_to": 2, "entries_replayed": 3, "entries_skipped": 0, "msg_id": 1}}
```

## 参考资料

- [ARIES Recovery Algorithm](https://en.wikipedia.org/wiki/Algorithms_for_Recovery_and_Isolation_Exploiting_Semantics)：The classic ARIES algorithm用于WAL-based crash recovery in databases

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
