# Prevent Split Votes Through Term Management

英文标题：Prevent Split Votes Through Term Management
网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-5-split-vote>

课程：5. 选举器：Leader Election
任务序号：5
短标题：Term Management
难度：advanced
子主题：Raft Leader 选举

## 中文导读

本题要求你完成 `Prevent Split Votes Through Term Management`。

重点关注：`term`、`split vote`、`election retry`。

建议先按提示逐步实现：Increment term when starting election。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Handle split votes where no Candidate receives a majority. Candidates increment their term和重试. Proper term management ensures the 集群 eventually elects a Leader.

## 概念说明

### Term Management

The term acts as a logical 时钟. Higher terms always win. When a 节点 sees a higher term, it immediately becomes a Follower. This prevents stale leaders from causing inconsistency.

## 涉及概念

- `term`
- `split vote`
- `election retry`

## 实现提示

- Increment term when starting election
- Step down if see higher term
- 重试 election on 超时

## 测试用例

### 1. Increment term on new 选举

节点 increments term from 1→2 when starting election, becomes Candidate, votes用于itself.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"set_term","msg_id":2,"term":1}}
{"src":"c0","dest":"n1","body":{"type":"trigger_election_timeout","msg_id":3}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":4}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"trigger_election_timeout_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":4,"msg_id":3,"state":"candidate","term":2}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
