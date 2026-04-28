# 实现基于树的广播覆盖网络

英文标题：Implement Tree-Based Broadcast Overlay
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-1-tree-broadcast>

课程：3. 传播者：Gossip 信息传播
任务序号：11
短标题：树广播
难度：进阶
子主题：Topology-Aware Gossip

## 中文导读

这道题要求你用生成树（Spanning Tree）来优化广播效率。随机八卦传播虽然简单，但会产生大量重复消息；而基于树的广播能保证每个节点只收到一份消息副本，大幅减少网络开销。理解树广播是学习拓扑感知型传播协议的基础。

## 题目说明

随机八卦传播会浪费消息，因为节点（Node）可能会重复收到同一条消息。**生成树（Spanning Tree）** 可以确保每个节点恰好只收到一份消息副本：根节点将消息广播给它的子节点，子节点再转发给各自的子节点，以此类推。

你需要实现基于树的广播机制：

1. 通过 `topology` 消息获取本节点的树邻居列表
2. 收到 `broadcast` 后，将消息转发给所有树邻居（发送方除外）
3. 记录转发路径，便于调试

需要处理以下消息类型：
- `topology`：存储本节点的邻居列表
- `broadcast`：存储值并转发给树邻居
- `read`：返回所有已知的值
- `tree_info`：返回本节点当前的树结构信息

```json
请求:  {"type": "tree_info", "msg_id": 1}
响应: {"type": "tree_info_ok", "in_reply_to": 1, "neighbors": ["n2", "n3"], "message_count": 5}
```

## 涉及概念

- `spanning tree`
- `tree broadcast`
- `overlay network`
- `message forwarding`

## 实现提示

- 根据 Maelstrom 提供的拓扑信息构建生成树
- 每个节点只向自己在树中的子节点转发消息
- 树广播的消息复杂度为 O(N-1)，而随机八卦传播为 O(N*K)，效率差距明显
- 根节点收到广播后，沿着树向下逐层推送
- 利用 `topology` 消息来获知自己的邻居节点

## 测试用例

### 1. 拓扑消息正确存储邻居

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":["n2","n3"],"n2":["n1"],"n3":["n1"]}}}
{"src":"c1","dest":"n1","body":{"type":"tree_info","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tree_info_ok", "neighbors": ["n2", "n3"], "message_count": 0, "in_reply_to": 3, "msg_id": 2}}
```

### 2. 广播后可正确读取

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

## 参考资料

- [Spanning Tree Protocol](https://en.wikipedia.org/wiki/Spanning_Tree_Protocol)：介绍网络中生成树概念的综述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
