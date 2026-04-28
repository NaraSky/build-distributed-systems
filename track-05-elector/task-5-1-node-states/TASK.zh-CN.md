# 实现节点States (Leader, Follower, Candidate)

英文标题：Implement节点States (Leader, Follower, Candidate)
网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-1-node-states>

课程：5. 选举器：Leader Election
任务序号：1
短标题：Node States
难度：intermediate
子主题：Raft Leader 选举

## 中文导读

本题要求你完成 `实现节点States (Leader, Follower, Candidate)`。

重点关注：`state machine`、`leader election`、`Raft roles`。

建议先按提示逐步实现：Define an enum用于states。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement the three states from Raft: Leader, Follower,和Candidate. Each 节点 starts as a Follower. Candidates 请求 votes. Leaders coordinate the 集群.

## 概念说明

### Raft Roles

In Raft, every 节点 is in one of three states: Follower (passive, responds to leaders), Candidate (seeking to become Leader), or Leader (handles all 客户端 requests). This clear state machine simplifies reasoning about the protocol.

## 涉及概念

- `state machine`
- `leader election`
- `Raft roles`

## 实现提示

- Define an enum用于states
- All 节点 start as followers
- State transitions happen on specific events

## 测试用例

### 1.节点starts as follower

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":2}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":2,"msg_id":1,"state":"follower","term":0}}
```

## 参考资料

- [Raft Paper](https://raft.github.io/raft.pdf)：In Search of an Understandable 共识 Algorithm

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
