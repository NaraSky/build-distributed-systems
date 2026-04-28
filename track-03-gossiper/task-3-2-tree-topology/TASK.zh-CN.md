# 构建树形拓扑广播

英文标题：Build Flat Tree Topology Gossip
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-tree-topology>

课程：3. 传播者：Gossip 信息传播
任务序号：2
短标题：树形拓扑
难度：进阶
子主题：朴素广播（洪泛）

## 中文导读

这道题让你用树形拓扑来优化广播。上一题的洪泛方式虽然简单，但消息量太大。通过把节点组织成一棵生成树，每条消息只沿着树的边传播一次，就能大幅减少消息数量。这是从"能用"到"好用"的第一步优化。

## 题目说明

利用树形拓扑来优化你的广播系统。不再向所有邻居洪泛，而是把节点组织成一棵生成树（Spanning Tree），让每条消息沿着树的边恰好传播一次。

这样可以把每次广播的消息复杂度从 O(n*m) 降低到 O(n)，其中 n 是节点数量。

## 概念说明

### 生成树

生成树（Spanning Tree）是一种用恰好 n-1 条边连接所有 n 个节点、且没有环的结构。沿着生成树广播可以保证每条消息只被传递到每个节点一次，从而最大限度地减少网络流量。

你可以把它想象成公司的组织架构树——消息从老板传到部门经理，再传到基层员工，每个人只需要通知自己的直接下属，既不会遗漏也不会重复。

## 涉及概念

- `tree topology`
- `spanning tree`
- `efficient propagation`

## 实现提示

- 利用系统提供的拓扑信息来构建树结构
- 避免将消息回传给发送者（父节点）
- 树形结构能保证消息数量为 O(n) 级别
- 先回复 `broadcast_ok`，再转发给邻居节点——这能确保输出中 `msg_id` 的顺序是确定性的

## 测试用例

### 1. 三节点的树形广播

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
