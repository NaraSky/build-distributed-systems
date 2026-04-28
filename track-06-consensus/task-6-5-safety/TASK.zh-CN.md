# 实现 选举 Restriction用于Safety

英文标题：Implement Election Restriction用于Safety
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-5-safety>

课程：6. 共识：Raft 与日志复制
任务序号：5
短标题：Safety
难度：advanced
子主题：Raft 日志 复制

## 中文导读

本题要求你完成 `实现 选举 Restriction用于Safety`。

重点关注：`election restriction`、`safety`、`up-to-date`。

建议先按提示逐步实现：Voter checks Candidate 日志 is up-to-date。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement the Election Restriction to ensure safety:

A Candidate must have an "up-to-date" 日志 to win election:
1. Voter compares own 日志 to Candidate's
2. If Candidate lastLogTerm > voter lastLogTerm: Candidate is ahead
3. If same term, compare lastLogIndex
4. Only grant vote if Candidate is at least as up-to-date

This ensures the elected Leader has all committed entries.

## 概念说明

### 选举 Restriction

This is the key safety property of Raft. By only electing candidates，包含up-to-date logs, we ensure no committed entries are lost. The Leader completeness property follows from this.

### Comparison Logic

Higher term always wins. If same term, longer 日志 wins. This captures "more up-to-date" precisely. A Leader elected under these rules has everything committed before it.

## 涉及概念

- `election restriction`
- `safety`
- `up-to-date`

## 实现提示

- Voter checks Candidate 日志 is up-to-date
- Compare last 日志 term first, then 索引
- Reject vote if Candidate 日志 is behind

## 测试用例

### 1. Grant vote to higher term

输入：

```json
{"src":"c0","dest":"n2","body":{"type":"init","msg_id":1,"node_id":"n2","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n2","body":{"type":"set_term","msg_id":2,"term":2}}
{"src":"n1","dest":"n2","body":{"type":"request_vote","msg_id":3,"term":3,"candidate_id":"n1","last_log_index":0,"last_log_term":0}}
```

期望输出：

```text
{"src":"n2","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n2","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n2","dest":"n1","body":{"type":"request_vote_ok","in_reply_to":3,"msg_id":2,"term":3,"vote_granted":true}}
```

## 参考资料

- [Raft Safety](https://raft.github.io/raft.pdf)：Raft paper section on safety

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
