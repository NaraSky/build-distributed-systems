# 构建 Flat Tree Topology Gossip

英文标题：Build Flat Tree Topology Gossip
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-tree-topology>

课程：3. 传播者：Gossip 信息传播
任务序号：2
短标题：Tree Topology
难度：intermediate
子主题：Naive 广播 (Flooding)

## 中文导读

本题要求你完成 `构建 Flat Tree Topology Gossip`。

重点关注：`tree topology`、`spanning tree`、`efficient propagation`。

建议先按提示逐步实现：Use the provided topology to form a tree。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Optimize your 广播 by使用a tree topology. Instead of flooding to all neighbors, organize 节点 into a spanning tree where each 消息 travels along tree edges exactly once.

This reduces 消息 complexity from O(n*m) to O(n)用于each 广播, where n is the number of 节点.

## 概念说明

### Spanning Trees

A spanning tree connects all 节点，包含exactly n-1 edges和no cycles. Broadcasting along a tree ensures each 消息 is delivered exactly once to each 节点, minimizing 网络 traffic.

## 涉及概念

- `tree topology`
- `spanning tree`
- `efficient propagation`

## 实现提示

- Use the provided topology to form a tree
- Avoid sending back to parent
- Tree ensures O(n) 消息
- Reply，包含broadcast_ok before forwarding to neighbors - this ensures deterministic msg_id ordering in the output

## 测试用例

### 1. Tree 广播，包含3 nodes

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":["n2"],"n2":["n1","n3"],"n3":["n2"]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":100}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c0", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "n2", "body": {"type": "broadcast", "message": 100, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [100], "in_reply_to": 4, "msg_id": 4}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
