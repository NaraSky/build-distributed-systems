# 实现 Entry Commitment

英文标题：Implement Entry Commitment
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-3-commitment>

课程：6. 共识：Raft 与日志复制
任务序号：3
短标题：Commitment
难度：advanced
子主题：Raft 日志 复制

## 中文导读

本题要求你完成 `实现 Entry Commitment`。

重点关注：`commitment`、`majority`、`quorum`。

建议先按提示逐步实现：Entry committed when on majority。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement 日志 entry commitment:

1. Leader tracks matchIndex用于each Follower
2. For each 索引 N, count how many 节点 have matchIndex >= N
3. If majority have entry N,和entry N is from current term, commit N
4. Advance commitIndex to highest committed N
5. Notify followers of new commitIndex in next 心跳

Important: Only commit entries from current term to satisfy the Raft safety property.

## 概念说明

### Commitment

An entry is committed when the Leader knows a majority have it. Committed entries are durable - they will survive Leader changes. The Leader advances commitIndex when majority confirms.

### Current Term Requirement

Leaders only directly commit entries from their own term. Entries from previous terms are committed indirectly when a current-term entry is committed after them. This prevents a subtle safety violation.

## 涉及概念

- `commitment`
- `majority`
- `quorum`

## 实现提示

- Entry committed when on majority
- Use matchIndex to count replicas
- Only commit entries from current term directly

## 测试用例

### 1. Commit on majority 复制

Multi-节点 test: Leader appends entry, waits用于majority acks (2 out of 3 节点), advances commitIndex. Verify entry from current term is committed.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [Raft Commitment](https://www.youtube.com/watch?v=YbZ3zDzDnrw)：MIT 6.824 Raft lecture

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
