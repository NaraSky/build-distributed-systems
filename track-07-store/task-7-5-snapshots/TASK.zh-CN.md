# 实现 日志 Compaction，包含Snapshots

英文标题：Implement Log Compaction，包含Snapshots
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-7-5-snapshots>

课程：7. 存储：线性一致 KV Store
任务序号：5
短标题：Snapshots
难度：advanced
子主题：Linearizable 键值 存储

## 中文导读

本题要求你完成 `实现 日志 Compaction，包含Snapshots`。

重点关注：`snapshot`、`log compaction`、`recovery`。

建议先按提示逐步实现：Snapshot state machine periodically。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement 日志 compaction，包含snapshots:

1. Periodically snapshot state machine state
2. Record snapshot 索引和term
3. Discard 日志 entries before snapshot
4. On recovery, restore from snapshot then replay 日志
5. Send InstallSnapshot to followers that are too far behind

This prevents unbounded 日志 growth.

## 概念说明

### 日志 Compaction

The Raft 日志 grows forever as commands arrive. Snapshots compress applied 日志 entries into a compact state representation. Only the snapshot和subsequent 日志 are needed用于recovery.

### InstallSnapshot RPC

When a Follower is so far behind that Leader discarded needed entries, send the snapshot instead. The Follower replaces its state，包含the snapshot和resumes from there.

## 涉及概念

- `snapshot`
- `log compaction`
- `recovery`

## 实现提示

- Snapshot state machine periodically
- Discard 日志 entries before snapshot
- Send snapshot to slow followers

## 测试用例

### 1. 创建 snapshot

Snapshot created，包含lastIncludedIndex=5, lastIncludedTerm=2, contains state {"x":1,"y":2}

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"seed_state","msg_id":2,"state":{"x":1,"y":2},"commit_index":5,"term":2}}
{"src":"c0","dest":"n1","body":{"type":"take_snapshot","msg_id":3,"up_to_index":5}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"seed_state_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"snapshot_ok","in_reply_to":3,"msg_id":2,"last_included_index":5,"last_included_term":2}}
```

## 参考资料

- [Raft Section 7](https://raft.github.io/raft.pdf)：日志 compaction in Raft

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
