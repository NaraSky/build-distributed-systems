# 添加定时周期性 Gossip 轮次

英文标题：Add Periodic Gossip Rounds on a Timer
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-3-gossip-timer>

课程：3. 传播者：Gossip 信息传播
任务序号：8
短标题：Gossip 定时器
难度：进阶
子主题：Gossip 协议

## 中文导读

这道题在之前的基础上更进一步：不再仅在收到新广播时才传播，而是加入定时器，每隔一段时间主动发起一轮 Gossip，把自己知道的所有消息同步给随机选择的节点。这样即使有消息在传播过程中丢失了，也能通过后续的定时同步得到恢复，从而保证最终收敛。

## 题目说明

不再仅仅在收到新广播消息时才进行 Gossip 传播，而是加入**周期性 Gossip 轮次**：每隔一个固定时间间隔，随机选择 K 个节点，把你知道的所有消息发送给它们。这样即使有消息在传输过程中丢失，也能确保系统最终收敛到一致状态。

实现 `gossip_round` 处理器，用于触发一轮 Gossip：
```json
Request:  {"type": "gossip_round", "msg_id": 1}
Response: {"type": "gossip_round_ok", "in_reply_to": 1, "peers_contacted": 2, "messages_sent": 5}
```

以及 `gossip_sync` 处理器，用于接收来自其他节点的完整状态：
```json
Request:  {"type": "gossip_sync", "msg_id": 1, "messages": [1, 2, 3]}
Response: {"type": "gossip_sync_ok", "in_reply_to": 1, "new_count": 2}
```

同步处理器将收到的消息与本地集合合并，并报告有多少条消息是新增的。

## 涉及概念

- `periodic gossip`
- `convergence time`
- `anti-entropy`
- `pull gossip`

## 实现提示

- 推送式 Gossip 在收到广播时发送消息；拉取式 Gossip 通过定期同步来传播
- 每轮 Gossip 会将所有已知消息与随机选择的节点进行对比同步
- 跟踪收敛过程：需要多少轮才能让所有节点拥有全部消息
- 定时器的间隔影响延迟和消息开销之间的权衡
- 将 `gossip_round` 实现为一种可由外部触发的消息类型，方便测试

## 测试用例

### 1. 没有消息时执行 Gossip 轮次不发送任何内容

验证说明：`gossip_round_ok` 应显示 `peers_contacted=2` 且 `messages_sent=0`（因为没有消息需要发送）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"gossip_round","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Gossip 同步合并新消息

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

- [Anti-Entropy Gossip Protocols](https://www.distributed-systems.net/my-data/papers/2007.osr.pdf)：关于推送式、拉取式和推拉式 Gossip 策略的综述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
