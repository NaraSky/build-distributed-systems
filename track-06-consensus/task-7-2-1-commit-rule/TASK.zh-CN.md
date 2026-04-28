# 实现 the Raft Commitment Rule

英文标题：Implement the Raft Commitment Rule
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-1-commit-rule>

课程：6. 共识：Raft 与日志复制
任务序号：6
短标题：Commit Rule
难度：intermediate
子主题：Commitment和Application

## 中文导读

本题要求你完成 `实现 the Raft Commitment Rule`。

重点关注：`commitment`、`majority replication`、`commitIndex`、`log replication`。

建议先按提示逐步实现：An entry is committed when a majority of 节点 have it in their 日志。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement the Raft commitment rule: an entry is committed when a majority of 节点 have it in their 日志. The Leader uses `matchIndex[]` to determine when this is true.

```JSON
请求:  {"type": "check_commit", "msg_id": 1, "log_length": 5, "match_indices": {"n1": 5, "n2": 5, "n3": 3, "n4": 2, "n5": 1}, "current_term": 3}
响应: {"type": "check_commit_ok", "in_reply_to": 1, "new_commit_index": 5, "majority_count": 2, "quorum": 3, "committed": true}

请求:  {"type": "advance_commit", "msg_id": 2, "old_commit_index": 3, "match_indices": {"n1": 7, "n2": 5, "n3": 5, "n4": 3, "n5": 2}, "current_term": 3}
响应: {"type": "advance_commit_ok", "in_reply_to": 2, "new_commit_index": 5, "entries_committed": 2}
```

## 涉及概念

- `commitment`
- `majority replication`
- `commitIndex`
- `log replication`

## 实现提示

- An entry is committed when a majority of 节点 have it in their 日志
- The Leader tracks matchIndex[]用于each Follower
- commitIndex advances when a majority of matchIndex values >= a given 索引
- Only entries from the current term can directly advance commitIndex
- Entries from previous terms are committed indirectly

## 测试用例

### 1. Majority 复制 commits entry

check_commit_ok should show new_commit_index: 3 since n1和n2 (majority of 3) have 索引 3.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"check_commit","msg_id":2,"log_length":3,"match_indices":{"n1":3,"n2":3,"n3":1},"current_term":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. No majority means no commit advance

Only 2 out of 5 have 索引 5. Quorum needs 3. committed: false.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4","n5"]}}
{"src":"c1","dest":"n1","body":{"type":"check_commit","msg_id":2,"log_length":5,"match_indices":{"n1":5,"n2":5,"n3":1,"n4":1,"n5":1},"current_term":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Raft Consensus - Log Commitment](https://raft.github.io/raft.pdf)：Raft paper Section 5.3-5.4 on commitment rules

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
