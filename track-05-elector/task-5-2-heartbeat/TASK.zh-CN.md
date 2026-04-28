# 添加 Heartbeat Mechanism

英文标题：Add Heartbeat Mechanism
网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-2-heartbeat>

课程：5. 选举器：Leader Election
任务序号：2
短标题：Heartbeat
难度：intermediate
子主题：Raft Leader 选举

## 中文导读

本题要求你完成 `添加 Heartbeat Mechanism`。

重点关注：`heartbeat`、`liveness`、`failure detection`。

建议先按提示逐步实现：Leader sends heartbeats periodically。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement heartbeats from the Leader to followers. The Leader periodically sends AppendEntries (empty用于now) to maintain authority. Followers that do not receive heartbeats become candidates.

## 概念说明

### Heartbeats

Heartbeats serve dual purposes: they prevent followers from starting elections,和they carry 日志 复制 data (in full Raft). A Leader that stops sending heartbeats will be replaced.

## 涉及概念

- `heartbeat`
- `liveness`
- `failure detection`

## 实现提示

- Leader sends heartbeats periodically
- Followers reset 超时 on 心跳
- Missing heartbeats trigger election

## 测试用例

### 1. Leader sends heartbeat

Leader sends 心跳 append_entries to all peers (n2, n3).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"become_leader","msg_id":2,"term":1}}
{"src":"c0","dest":"n1","body":{"type":"wait","msg_id":3,"duration_ms":150}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"become_leader_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"n2","body":{"type":"append_entries","msg_id":2,"term":1,"leader_id":"n1","prev_log_index":0,"prev_log_term":0,"entries":[],"leader_commit":0}}
{"src":"n1","dest":"n3","body":{"type":"append_entries","msg_id":3,"term":1,"leader_id":"n1","prev_log_index":0,"prev_log_term":0,"entries":[],"leader_commit":0}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
