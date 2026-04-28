# 实现基础广播：让所有节点收到消息

英文标题：Implement Basic Broadcast to All Nodes
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-1-basic-broadcast>

课程：3. 传播者：Gossip 信息传播
任务序号：1
短标题：基础广播
难度：入门
子主题：朴素广播（洪泛）

## 中文导读

这道题要求你实现一个最基础的广播系统——当任意一个节点（Node）收到一条消息后，这条消息最终要传播到集群中的所有节点。这是分布式系统中信息传播的起点，理解了它，后续的优化才有基础。

## 题目说明

实现一个广播系统，使得发送到任意节点的消息最终能够到达所有节点。

你需要处理三种消息类型：
1. `topology`：告诉你当前节点在集群拓扑中的邻居有哪些
2. `broadcast`：携带一个需要传播的消息值
3. `read`：返回当前节点已经收到的所有消息

当你收到一条广播消息时，需要把它存储下来，并转发给你的邻居节点。收到读取请求时，返回目前为止收到的所有不重复的消息。

## 概念说明

### 广播协议

广播（Broadcast）是许多分布式算法的基础。当一个节点获得了某条信息，它必须把这条信息分享给集群中的其他节点。难点在于如何高效地完成传播，同时避免产生消息风暴。

### 洪泛

最简单的广播方式就是洪泛（Flooding）：把每条消息都转发给所有邻居。这种方式能保证消息一定能送达，但消息数量是 O(n*m) 级别的（n 是节点数，m 是消息数）。后续的任务中我们会优化这个问题。

你可以把洪泛想象成一个人在办公室里大喊一声消息，然后每个听到的人也都跟着大喊，直到整个办公室的人都听到了——简单粗暴但确实有效。

## 涉及概念

- `broadcast`
- `flooding`
- `message propagation`

## 实现提示

- 用一个集合来存储已收到的消息
- 将新消息转发给所有已知的节点
- 处理 `topology` 消息以获取邻居信息

## 测试用例

### 1. 基础广播与读取

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":100}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c0", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [100], "in_reply_to": 4, "msg_id": 3}}
```

### 2. 广播多条消息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":"msg1"}}
{"src":"c2","dest":"n1","body":{"type":"broadcast","msg_id":4,"message":"msg2"}}
{"src":"c3","dest":"n1","body":{"type":"read","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c0", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c2", "body": {"type": "broadcast_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "n1", "dest": "c3", "body": {"type": "read_ok", "messages": ["msg1", "msg2"], "in_reply_to": 5, "msg_id": 4}}
```

## 参考资料

- [Broadcast Challenge](https://fly.io/dist-sys/3a/)：Fly.io Gossip Glomers 广播挑战题

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
