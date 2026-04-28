# 添加心跳机制

网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-2-heartbeat>

课程：5. 选举器：领导者选举
任务序号：2
短标题：心跳
难度：进阶
子主题：Raft 领导者选举

## 中文导读

这道题让你实现领导者向跟随者发送心跳的机制。领导者定期发送空的日志追加消息来维持权威，跟随者如果长时间没有收到心跳就会认为领导者已经失联，从而发起新的选举。心跳是 Raft 中维持集群稳定的关键机制。

## 题目说明

实现从领导者到跟随者的心跳机制。领导者定期发送 AppendEntries 消息（目前为空，不携带日志条目）来维持自己的权威。如果跟随者在超时时间内没有收到心跳，就会变成候选人发起选举。

## 概念说明

### 心跳

心跳有双重作用：一是阻止跟随者发起新的选举（"领导者还活着，不用选了"），二是在完整的 Raft 实现中还会携带日志复制数据。如果领导者停止发送心跳（比如宕机或网络隔离），它会被新选出的领导者替换。这就像团队队长需要定期发消息告诉大家"我还在"，如果长时间没消息，大家就会重新选队长。

## 涉及概念

- `heartbeat`
- `liveness`
- `failure detection`

## 实现提示

- 领导者定期发送心跳消息
- 跟随者收到心跳时重置超时计时器
- 超时未收到心跳会触发选举

## 测试用例

### 1. 领导者发送心跳

领导者向所有邻居节点（n2、n3）发送心跳 append_entries 消息。

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
