# 实现 WAL Compaction，包含Atomic Snapshot

英文标题：Implement WAL Compaction，包含Atomic Snapshot
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-4-compaction>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：4
短标题：WAL Compaction
难度：advanced
子主题：The Commit 日志 (WAL)

## 中文导读

本题要求你完成 `实现 WAL Compaction，包含Atomic Snapshot`。

重点关注：`log compaction`、`snapshot`、`truncation`、`atomic operation`、`space reclamation`。

建议先按提示逐步实现：Once a snapshot of the state machine is taken, old WAL entries become unnecessary。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Without compaction, the WAL grows forever. Every database solves this，包含the same pattern: periodically take a **snapshot** of the state machine, then **truncate** all WAL entries before the snapshot.

The compaction algorithm:
1. Serialize the current state machine to a snapshot file
2. Record the WAL offset at which the snapshot was taken
3. Delete all WAL entries (segments) before that offset
4. On recovery: load the snapshot, then replay only entries after the snapshot offset

The critical requirement: **atomicity**. If the system crashes between taking the snapshot和truncating the WAL, there must be no data loss. The standard approach:
- Write snapshot to a temp file
- Atomically rename the temp file to the final snapshot path
- Only then delete old WAL segments

```JSON
请求:  {"type": "wal_snapshot", "msg_id": 1}
响应: {"type": "wal_snapshot_ok", "in_reply_to": 1, "snapshot_offset": 500, "snapshot_size_bytes": 2048}

请求:  {"type": "wal_compact", "msg_id": 2, "snapshot_at_offset": 500}
响应: {"type": "wal_compact_ok", "in_reply_to": 2, "snapshot_offset": 500, "entries_before": 1000, "entries_after": 500, "bytes_freed": 32000}
```

## 涉及概念

- `log compaction`
- `snapshot`
- `truncation`
- `atomic operation`
- `space reclamation`

## 实现提示

- Once a snapshot of the state machine is taken, old WAL entries become unnecessary
- The process: take snapshot -> record snapshot offset -> delete WAL entries before that offset
- The snapshot + truncation MUST be atomic: a crash between them means data loss
- Write the snapshot to a temp file, then atomically rename it into place
- On recovery: load snapshot first, then replay only WAL entries after the snapshot offset

## 测试用例

### 1. Take a snapshot of current state

wal_snapshot_ok should contain snapshot_offset >= 2和snapshot_size_bytes > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"set x=1"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":3,"payload":"set y=2"}}
{"src":"c1","dest":"n1","body":{"type":"wal_snapshot","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compaction frees old entries

wal_compact_ok should show entries_after < entries_before和bytes_freed > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_compact","msg_id":2,"snapshot_at_offset":500}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Log Compaction in Kafka](https://kafka.apache.org/documentation/#compaction)：How Kafka implements 日志 compaction to reclaim disk space while keeping latest values

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
