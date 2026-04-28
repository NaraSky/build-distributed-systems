# 实现 Gossip 扇出与随机节点选择

网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-1-gossip-fanout>

课程：3. 传播者：Gossip 信息传播
任务序号：6
短标题：Gossip 扇出
难度：进阶
子主题：Gossip 协议

## 中文导读

想象一个人听到一条消息后，不是对着所有人大喊，而是随机告诉身边几个人，这几个人再各自告诉身边几个人。用不了多久，所有人就都知道了。这就是 Gossip 协议（流言协议）的工作原理。

这道题让你实现 Gossip 协议的核心机制——扇出（Fanout）。每个节点收到新消息后，随机选择 K 个节点转发，而不是广播给所有人。这种方式没有单点故障，非常健壮。

## 题目说明

Gossip 协议用概率性的方式传播信息：每个节点不是把消息广播给所有节点，而是只转发给随机选出的 K 个节点。这种方式比基于树的广播更加可靠，因为不存在某个节点挂了就全断的问题。

你需要实现以下功能：

1. 维护一个已知消息的集合（已见集合），用来记录收到过哪些消息
2. 收到 `broadcast` 消息时，把消息值加入已见集合
3. 把这个值转发给随机选出的 K 个节点（默认 K=2），这就是"扇出"
4. 收到 `read` 消息时，返回所有已知的消息值
5. 记录 Gossip 的统计信息

```json
Broadcast: {"type": "broadcast", "msg_id": 1, "message": 42}
Response:  {"type": "broadcast_ok", "in_reply_to": 1}

Read:     {"type": "read", "msg_id": 2}
Response: {"type": "read_ok", "in_reply_to": 2, "messages": [42]}
```

## 涉及概念

- `gossip protocol`
- `fanout`
- `random peer selection`
- `probabilistic broadcast`

## 实现提示

- 每轮 Gossip 时，从集群中随机选择 K 个节点
- 不要把消息发给自己，也不要发给消息的来源节点
- 建议从扇出 K=2 开始，这已经能提供不错的覆盖率
- 选择节点时使用无放回抽样，确保不会重复选中同一个节点
- 记录哪些消息已经见过，避免对同一条消息重复传播

## 测试用例

### 1. 广播消息并回复确认

节点应先输出 `init_ok`，然后向随机节点发送 Gossip 消息，再回复 `broadcast_ok`。Gossip 消息和确认回复的顺序可能不固定。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":42}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 读取返回所有已收到的消息

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

- [Epidemic Algorithms for Replicated Database Maintenance](https://dl.acm.org/doi/10.1145/41840.41841)：Demers 等人于 1987 年发表的经典论文，首次系统性地研究了基于 Gossip 的数据库复制方法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
