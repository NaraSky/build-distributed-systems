#处理Leader Changes，包含No-Op on 选举

英文标题：Handle Leader Changes，包含No-Op on Election
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-3-noop-on-election>

课程：6. 共识：Raft 与日志复制
任务序号：8
短标题：No-Op on 选举
难度：advanced
子主题：Commitment和Application

## 中文导读

本题要求你完成 `Handle Leader Changes，包含No-Op on 选举`。

重点关注：`no-op entry`、`leader change`、`uncommitted entries`、`safety`。

建议先按提示逐步实现：A new Leader cannot know which entries from previous terms are committed。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a new Leader is elected, it must not apply uncommitted entries from previous terms. The "no-op on election" trick solves this: the new Leader immediately appends a no-op entry in its own term. Once this no-op is committed (majority replicated), all prior entries are also committed.

```JSON
请求:  {"type": "leader_change", "msg_id": 1, "new_leader": "n2", "new_term": 3, "日志": [
    {"索引": 1, "term": 1, "command": {"op": "put", "key": "x", "value": "1"}},
    {"索引": 2, "term": 2, "command": {"op": "put", "key": "y", "value": "2"}},
    {"索引": 3, "term": 2, "command": {"op": "put", "key": "z", "value": "3"}}
], "commit_index": 1}
响应: {"type": "leader_change_ok", "in_reply_to": 1, "noop_appended_at": 4, "noop_term": 3, "safe_to_apply_after_commit": true}

请求:  {"type": "simulate_noop_commit", "msg_id": 2, "noop_index": 4}
响应: {"type": "simulate_noop_commit_ok", "in_reply_to": 2, "new_commit_index": 4, "entries_now_committed": [2, 3, 4]}
```

## 涉及概念

- `no-op entry`
- `leader change`
- `uncommitted entries`
- `safety`

## 实现提示

- A new Leader cannot know which entries from previous terms are committed
- The no-op trick: new Leader appends a no-op entry in its own term
- Once the no-op is committed, all prior entries are also committed
- This avoids the problem of a new Leader applying uncommitted old entries
- The no-op is a dummy command that does not modify state

## 测试用例

### 1. New Leader appends no-op

leader_change_ok should show noop_appended_at: 2和noop_term: 3.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"leader_change","msg_id":2,"new_leader":"n1","new_term":3,"log":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}}],"commit_index":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. No-op commit advances all prior entries

simulate_noop_commit_ok should show new_commit_index: 3, entries_now_committed: [1, 2, 3].

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"leader_change","msg_id":2,"new_leader":"n1","new_term":2,"log":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":"2"}}],"commit_index":0}}
{"src":"c1","dest":"n1","body":{"type":"simulate_noop_commit","msg_id":3,"noop_index":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Raft - Committing entries from previous terms](https://raft.github.io/raft.pdf)：Raft paper Section 5.4.2 on the no-op trick用于safe commitment

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
