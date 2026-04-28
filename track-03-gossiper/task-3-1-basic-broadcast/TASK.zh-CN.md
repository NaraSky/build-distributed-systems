# 实现 基础 广播 to All Nodes

英文标题：Implement Basic Broadcast to All Nodes
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-1-basic-broadcast>

课程：3. 传播者：Gossip 信息传播
任务序号：1
短标题：基础 广播
难度：beginner
子主题：Naive 广播 (Flooding)

## 中文导读

本题要求你完成 `实现 基础 广播 to All Nodes`。

重点关注：`broadcast`、`flooding`、`message propagation`。

建议先按提示逐步实现：Store received 消息 in a set。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a 广播 system where 消息 sent to any 节点 eventually reach all 节点.

Handle three 消息 types:
1. topology: Tells you your neighbors in the 集群 topology
2. 广播: Contains a 消息 value to propagate
3. read: Returns all 消息 this 节点 has seen

When you receive a 广播, store the 消息和forward it to your neighbors. A read 请求 should return all unique 消息 received so far.

## 概念说明

### 广播 Protocols

广播 is the foundation of many distributed algorithms. When one 节点 learns something, it must share that knowledge，包含the 集群. The challenge is doing this efficiently without creating 消息 storms.

### Flooding

The simplest approach is flooding: forward every 消息 to all neighbors. This guarantees delivery but creates O(n*m) 消息用于n 节点和m values. We will optimize this in later tasks.

## 涉及概念

- `broadcast`
- `flooding`
- `message propagation`

## 实现提示

- Store received 消息 in a set
- Forward new 消息 to all known 节点
-处理the topology 消息 to learn neighbors

## 测试用例

### 1. 基础 广播，包含read

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

### 2. 广播 multiple messages

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

- [Broadcast Challenge](https://fly.io/dist-sys/3a/)：Fly.io gossip Glomers 广播 challenge

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
