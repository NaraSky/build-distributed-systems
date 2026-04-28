# 添加 Snapshot Support用于日志 Compaction

英文标题：Add Snapshot Support用于Log Compaction
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-4-snapshot>

课程：6. 共识：Raft 与日志复制
任务序号：9
短标题：Snapshots
难度：advanced
子主题：Commitment和Application

## 中文导读

本题要求你完成 `添加 Snapshot Support用于日志 Compaction`。

重点关注：`snapshot`、`log compaction`、`InstallSnapshot RPC`、`state transfer`。

建议先按提示逐步实现：When the 日志 exceeds a threshold (e.g., 1000 entries), take a snapshot of the state machine。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Add snapshot support to compact the Raft 日志. When the 日志 grows beyond a threshold, take a snapshot of the state machine. Followers that fall behind receive the snapshot instead of individual 日志 entries.

```JSON
请求:  {"type": "take_snapshot", "msg_id": 1, "threshold": 5}
响应: {"type": "take_snapshot_ok", "in_reply_to": 1, "snapshot_index": 5, "snapshot_term": 2, "state_size_bytes": 256, "log_entries_trimmed": 5}

请求:  {"type": "install_snapshot", "msg_id": 2, "snapshot_index": 5, "snapshot_term": 2, "state": {"x": "1", "y": "2", "z": "3"}}
响应: {"type": "install_snapshot_ok", "in_reply_to": 2, "applied": true, "new_last_applied": 5}

请求:  {"type": "get_log_info", "msg_id": 3}
响应: {"type": "get_log_info_ok", "in_reply_to": 3, "first_index": 6, "last_index": 8, "snapshot_index": 5, "total_entries": 3}
```

## 涉及概念

- `snapshot`
- `log compaction`
- `InstallSnapshot RPC`
- `state transfer`

## 实现提示

- When the 日志 exceeds a threshold (e.g., 1000 entries), take a snapshot of the state machine
- The snapshot captures the full state at a given 索引和term
- After snapshotting, entries up to that 索引 can be discarded from the 日志
- Followers that fall too far behind receive the snapshot via InstallSnapshot RPC
- The snapshot replaces the state machine state和日志 up to snapshot 索引

## 测试用例

### 1. Take snapshot trims 日志

take_snapshot_ok should show snapshot_index: 3和log_entries_trimmed: 3.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":"2"}},{"index":3,"term":1,"command":{"op":"put","key":"z","value":"3"}}]}}
{"src":"c1","dest":"n1","body":{"type":"take_snapshot","msg_id":3,"threshold":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Install snapshot restores state

install_snapshot_ok，包含applied: true. get_state_ok should show state: {"a": "1", "b": "2"}.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"install_snapshot","msg_id":2,"snapshot_index":5,"snapshot_term":2,"state":{"a":"1","b":"2"}}}
{"src":"c1","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Raft - Log Compaction](https://raft.github.io/raft.pdf)：Raft paper Section 7 on 日志 compaction和snapshots

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
