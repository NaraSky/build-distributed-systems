# 实现 Randomized 选举 超时

英文标题：Implement Randomized Election Timeout
网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-3-election-timeout>

课程：5. 选举器：Leader Election
任务序号：3
短标题：选举 超时
难度：intermediate
子主题：Raft Leader 选举

## 中文导读

本题要求你完成 `实现 Randomized 选举 超时`。

重点关注：`randomization`、`timeout`、`split brain prevention`。

建议先按提示逐步实现：Use random 超时 between 150-300ms。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Add randomized election timeouts. When a Follower does not hear from a Leader within its 超时, it becomes a Candidate. Randomization helps prevent multiple 节点 from starting elections simultaneously.

## 概念说明

### Randomized Timeouts

If all 节点 used the same 超时, 网络 hiccups could cause multiple simultaneous elections, splitting votes和delaying Leader selection.随机timeouts spread out elections, usually letting one 节点 win quickly.

## 涉及概念

- `randomization`
- `timeout`
- `split brain prevention`

## 实现提示

- Use random 超时 between 150-300ms
- Reset 超时 on 心跳
- Different timeouts reduce split votes

## 测试用例

### 1.随机超时 in range 150-300ms

Each 响应 contains a timeout_ms field in range 150-300. Values should vary due to randomization.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":2}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":3}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":4}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":4,"msg_id":3}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
