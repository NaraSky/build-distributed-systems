#处理Tree节点Failure，包含Direct Fallback

英文标题：Handle Tree节点Failure，包含Direct Fallback
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-2-tree-failure>

课程：3. 传播者：Gossip 信息传播
任务序号：12
短标题：Tree Failure
难度：advanced
子主题：Topology-Aware Gossip

## 中文导读

本题要求你完成 `Handle Tree节点Failure，包含Direct Fallback`。

重点关注：`fault tolerance`、`tree failure`、`ack timeout`、`direct delivery`。

建议先按提示逐步实现：When a child 节点 crashes, the entire subtree below it goes dark。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Tree 广播 is efficient but fragile: if a 节点 crashes, all its descendants lose connectivity. Your task is to add **故障 detection**，包含direct fallback.

When forwarding to a neighbor, expect a `broadcast_ack` within a 超时. If no ack arrives, fall back to direct delivery to all known 节点 that might be in the failed subtree.

Implement:
1. `广播`，包含ack tracking
2. `broadcast_ack` handler用于acknowledgments
3. `check_acks` handler to simulate 超时 checking和trigger fallback
4. `failure_stats` to report failures

```JSON
请求:  {"type": "check_acks", "msg_id": 1}
响应: {"type": "check_acks_ok", "in_reply_to": 1, "pending": 2, "timed_out": 1, "direct_sent": 3}
```

```JSON
请求:  {"type": "failure_stats", "msg_id": 2}
响应: {"type": "failure_stats_ok", "in_reply_to": 2, "total_failures": 1, "direct_deliveries": 3}
```

## 涉及概念

- `fault tolerance`
- `tree failure`
- `ack timeout`
- `direct delivery`

## 实现提示

- When a child 节点 crashes, the entire subtree below it goes dark
- Track acknowledgments from children，包含timeouts
- If no ack within 500ms, send directly to known downstream 节点
- Maintain a list of all 节点用于direct fallback
- 日志 failed deliveries to 标准错误用于debugging

## 测试用例

### 1. 广播，包含no neighbors

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [42], "in_reply_to": 4, "msg_id": 3}}
```

### 2. Failure stats initially zero

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"failure_stats","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "failure_stats_ok", "total_failures": 0, "direct_deliveries": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Fault-Tolerant Broadcast](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/2003-reliable-scalable.pdf)：Cornell research on reliable 广播 in unreliable networks

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
