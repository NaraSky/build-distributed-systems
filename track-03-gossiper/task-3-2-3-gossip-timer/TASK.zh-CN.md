# 添加 Periodic Gossip Rounds on a Timer

英文标题：Add Periodic Gossip Rounds on a Timer
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-3-gossip-timer>

课程：3. 传播者：Gossip 信息传播
任务序号：8
短标题：Gossip Timer
难度：intermediate
子主题：Gossip Protocol

## 中文导读

本题要求你完成 `添加 Periodic Gossip Rounds on a Timer`。

重点关注：`periodic gossip`、`convergence time`、`anti-entropy`、`pull gossip`。

建议先按提示逐步实现：Push gossip sends on 广播; pull gossip syncs periodically。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Instead of only gossiping when a new 广播 arrives, add **periodic gossip rounds**: every interval, pick K random peers和send them all your known 消息. This ensures convergence even if 消息 are dropped.

Implement a `gossip_round` handler that triggers a single gossip round:
```JSON
请求:  {"type": "gossip_round", "msg_id": 1}
响应: {"type": "gossip_round_ok", "in_reply_to": 1, "peers_contacted": 2, "messages_sent": 5}
```

And a `gossip_sync` handler that receives a full state from a peer:
```JSON
请求:  {"type": "gossip_sync", "msg_id": 1, "消息": [1, 2, 3]}
响应: {"type": "gossip_sync_ok", "in_reply_to": 1, "new_count": 2}
```

The sync handler merges the received 消息，包含the local set和reports how many were new.

## 涉及概念

- `periodic gossip`
- `convergence time`
- `anti-entropy`
- `pull gossip`

## 实现提示

- Push gossip sends on 广播; pull gossip syncs periodically
- A gossip round checks all known 消息 against a random peer
- Track convergence: how many rounds until all 节点 have all 消息
- The timer interval affects latency vs 消息 overhead tradeoff
- Implement gossip_round as a 消息 type triggered externally用于testing

## 测试用例

### 1. Gossip round，包含no messages sends nothing

gossip_round_ok should show peers_contacted=2和messages_sent=0 (no 消息 to send).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"gossip_round","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Gossip sync merges new messages

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":10}}
{"src":"n2","dest":"n1","body":{"type":"gossip_sync","msg_id":3,"messages":[10,20,30]}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "gossip_sync_ok", "new_count": 2, "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [10, 20, 30], "in_reply_to": 4, "msg_id": 3}}
```

## 参考资料

- [Anti-Entropy Gossip Protocols](https://www.distributed-systems.net/my-data/papers/2007.osr.pdf)：Overview of push, pull,和push-pull gossip strategies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
