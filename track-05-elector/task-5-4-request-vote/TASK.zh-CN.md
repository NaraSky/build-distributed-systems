#处理RequestVote RPC

英文标题：Handle RequestVote RPC
网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-4-request-vote>

课程：5. 选举器：Leader Election
任务序号：4
短标题：RequestVote
难度：advanced
子主题：Raft Leader 选举

## 中文导读

本题要求你完成 `Handle RequestVote RPC`。

重点关注：`voting`、`term comparison`、`vote granting`。

建议先按提示逐步实现：Grant vote if Candidate term >= current term。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement the RequestVote RPC. Candidates 请求 votes from other 节点. 节点 grant their vote if the Candidate's term is current和they have not already voted in this term.

## 概念说明

### Vote Granting

A 节点 grants its vote if: the Candidate term is at least as recent as its own,和it has not voted用于another Candidate in this term. This ensures at most one Leader per term.

## 涉及概念

- `voting`
- `term comparison`
- `vote granting`

## 实现提示

- Grant vote if Candidate term >= current term
- Only vote once per term
- Update term if Candidate has higher term

## 测试用例

### 1. Grant vote to same term candidate

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"set_term","msg_id":2,"term":2}}
{"src":"n2","dest":"n1","body":{"type":"request_vote","msg_id":3,"term":2,"candidate_id":"n2","last_log_index":0,"last_log_term":0}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"n2","body":{"type":"request_vote_ok","in_reply_to":3,"msg_id":2,"term":2,"vote_granted":true}}
```

## 参考资料

- [Raft Lecture](https://www.youtube.com/watch?v=YbZ3zDzDnrw)：MIT 6.824 Raft lecture by Robert Morris

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
