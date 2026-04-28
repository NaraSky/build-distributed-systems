# 实现 Tree-Based 广播 Overlay

英文标题：Implement Tree-Based Broadcast Overlay
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-1-tree-broadcast>

课程：3. 传播者：Gossip 信息传播
任务序号：11
短标题：Tree 广播
难度：intermediate
子主题：Topology-Aware Gossip

## 中文导读

本题要求你完成 `实现 Tree-Based 广播 Overlay`。

重点关注：`spanning tree`、`tree broadcast`、`overlay network`、`message forwarding`。

建议先按提示逐步实现：Build a spanning tree from the topology provided by Maelstrom。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Random gossip wastes 消息 because 节点 may receive duplicates. A **spanning tree** ensures each 节点 receives exactly one copy: the root broadcasts to its children, who forward to their children, etc.

Your task is to implement tree-based 广播:

1. Use the `topology` 消息 to learn your tree neighbors
2. On `广播`, forward to all tree neighbors except the source
3. Track the forwarding path用于debugging

Handle these 消息 types:
- `topology`: Store the neighbor list用于this 节点
- `广播`: Store value和forward to tree neighbors
- `read`: Return all known values
- `tree_info`: Return current tree structure用于this 节点

```JSON
请求:  {"type": "tree_info", "msg_id": 1}
响应: {"type": "tree_info_ok", "in_reply_to": 1, "neighbors": ["n2", "n3"], "message_count": 5}
```

## 涉及概念

- `spanning tree`
- `tree broadcast`
- `overlay network`
- `message forwarding`

## 实现提示

- Build a spanning tree from the topology provided by Maelstrom
- Each 节点 only forwards to its children in the tree
- Tree 广播 has O(N-1) 消息 vs O(N*K)用于random gossip
- The root receives the 广播和pushes down the tree
- Use the topology 消息 to learn your neighbors

## 测试用例

### 1. Topology stores neighbors

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

### 2. 广播 stores和reads back

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

- [Spanning Tree Protocol](https://en.wikipedia.org/wiki/Spanning_Tree_Protocol)：Overview of spanning tree concepts in networking

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
