#处理Concurrent Increments Across Multiple Nodes

英文标题：Handle并发Increments Across Multiple Nodes
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-5-concurrent-increments>

课程：4. 计数器：分布式状态与 CRDT
任务序号：5
短标题：Concurrent Updates
难度：advanced
子主题：The Lost Update Problem

## 中文导读

本题要求你完成 `Handle并发Increments Across Multiple Nodes`。

重点关注：`concurrent operations`、`distributed testing`、`verification`。

建议先按提示逐步实现：Periodically gossip your G-计数器 state。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Test your G-计数器 under heavy concurrent load. Multiple 节点 will simultaneously increment和the final value must equal the sum of all increments.

## 概念说明

### Eventual Consistency

With proper CRDT implementation, all 节点 will eventually converge to the same value. The G-计数器 guarantees this even under 网络 partitions和arbitrary 消息 delays.

## 涉及概念

- `concurrent operations`
- `distributed testing`
- `verification`

## 实现提示

- Periodically gossip your G-计数器 state
- Merge received states into yours
- All 节点 should converge to same value

## 测试用例

### 1. Local increments accumulate correctly

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":10}}
{"src":"c2","dest":"n1","body":{"type":"add","msg_id":3,"delta":20}}
{"src":"c3","dest":"n1","body":{"type":"add","msg_id":4,"delta":30}}
{"src":"c4","dest":"n1","body":{"type":"read","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c2", "body": {"type": "add_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c3", "body": {"type": "add_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "n1", "dest": "c4", "body": {"type": "read_ok", "value": 60, "in_reply_to": 5, "msg_id": 4}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
