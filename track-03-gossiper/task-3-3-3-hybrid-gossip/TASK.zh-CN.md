# 实现 Hybrid Tree和Gossip 广播

英文标题：Implement Hybrid Tree和Gossip Broadcast
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-3-hybrid-gossip>

课程：3. 传播者：Gossip 信息传播
任务序号：13
短标题：Hybrid Gossip
难度：advanced
子主题：Topology-Aware Gossip

## 中文导读

本题要求你完成 `实现 Hybrid Tree和Gossip 广播`。

重点关注：`hybrid broadcast`、`tree overlay`、`gossip fallback`、`convergence speed`。

建议先按提示逐步实现：First hop uses the tree用于fast delivery (low latency)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Pure tree 广播 is fast but fragile. Pure gossip is reliable but slow和wasteful. A **hybrid** approach uses tree用于the first hop (fast, efficient)和gossip用于reliability (catch stragglers).

Implement a hybrid 广播:
1. On 广播, forward via tree neighbors immediately
2. Periodically gossip all known 消息 to random peers (catch-up)
3. Track delivery path用于each 消息 (tree vs gossip)

```JSON
请求:  {"type": "delivery_info", "msg_id": 1, "value": 42}
响应: {"type": "delivery_info_ok", "in_reply_to": 1, "value": 42, "delivered_via": "tree", "hops": 1}
```

```JSON
请求:  {"type": "hybrid_stats", "msg_id": 2}
响应: {"type": "hybrid_stats_ok", "in_reply_to": 2, "tree_deliveries": 8, "gossip_deliveries": 2, "total": 10}
```

## 涉及概念

- `hybrid broadcast`
- `tree overlay`
- `gossip fallback`
- `convergence speed`

## 实现提示

- First hop uses the tree用于fast delivery (low latency)
- Background gossip rounds catch any missed 节点 (high reliability)
- Track whether each 消息 was delivered via tree or gossip
- Compare convergence speed of pure tree, pure gossip,和hybrid
- The hybrid approach gives the best of both worlds

## 测试用例

### 1. 广播 via tree tracks delivery

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"delivery_info","msg_id":4,"value":42}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "delivery_info_ok", "value": 42, "delivered_via": "tree", "hops": 0, "in_reply_to": 4, "msg_id": 3}}
```

### 2. Hybrid stats，包含zero messages

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hybrid_stats","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hybrid_stats_ok", "tree_deliveries": 0, "gossip_deliveries": 0, "total": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Plumtree: Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf)：Paper on combining tree和gossip用于efficient 广播

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
