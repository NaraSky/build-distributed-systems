# 实现 Gossip Fanout，包含Random Peer Selection

英文标题：Implement Gossip Fanout，包含Random Peer Selection
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-1-gossip-fanout>

课程：3. 传播者：Gossip 信息传播
任务序号：6
短标题：Gossip Fanout
难度：intermediate
子主题：Gossip Protocol

## 中文导读

本题要求你完成 `实现 Gossip Fanout，包含Random Peer Selection`。

重点关注：`gossip protocol`、`fanout`、`random peer selection`、`probabilistic broadcast`。

建议先按提示逐步实现：Pick K random peers from the 集群 on each gossip round。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

gossip protocols spread information probabilistically: instead of broadcasting to all 节点, each 节点 forwards to K random peers. This is more resilient than tree-based 广播 because there is no single point of 故障.

Your task is to implement gossip fanout:

1. Maintain a set of known 消息 (seen set)
2. On receiving a `广播` 消息, add the value to the seen set
3. Forward (gossip) the value to K random peers (default K=2)
4. On receiving a `read` 消息, return all known values
5. Track gossip statistics

```JSON
广播: {"type": "广播", "msg_id": 1, "消息": 42}
响应:  {"type": "broadcast_ok", "in_reply_to": 1}

Read:     {"type": "read", "msg_id": 2}
响应: {"type": "read_ok", "in_reply_to": 2, "消息": [42]}
```

## 涉及概念

- `gossip protocol`
- `fanout`
- `random peer selection`
- `probabilistic broadcast`

## 实现提示

- Pick K random peers from the 集群 on each gossip round
- Do not gossip to yourself or to the 消息 source
- Start，包含fanout K=2用于reasonable coverage
- Use random.sample to select peers without replacement
- Track which 消息 you have already seen to avoid re-gossip

## 测试用例

### 1. 广播 stores value和replies ok

Should output init_ok, then gossip 消息 to peers, then broadcast_ok. Order of gossip vs ok may vary.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":42}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read returns stored messages

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":10}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":20}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [10, 20], "in_reply_to": 4, "msg_id": 3}}
```

## 参考资料

- [Epidemic Algorithms用于Replicated Database Maintenance](https://dl.acm.org/doi/10.1145/41840.41841)：Original 1987 paper on gossip-based 复制 by Demers et al.

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
