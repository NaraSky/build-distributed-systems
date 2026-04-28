# 通过 Gossip 协议在集群中复制 PN-Counter

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-4-gossip-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：9
短标题：Gossip 计数器
难度：高级
子主题：G-Counter 与 PN-Counter

## 中文导读

这道题让你通过 gossip 协议将 PN-Counter 的状态在集群中复制。每个节点定期随机选择几个邻居，把自己的完整状态发过去，收到消息的节点将其与本地状态合并。这种方式像"传八卦"一样简单却有效，能保证所有节点最终收敛到一致的状态。

## 题目说明

为了在集群中复制 PN-Counter，每个节点定期将自己的完整状态通过 gossip 协议发送给随机选择的邻居节点。这是一种反熵（Anti-Entropy）协议，能保证最终一致性。

**Gossip 协议流程**：
1. 每隔 100 毫秒，从节点列表中随机选择 2 个邻居
2. 将你的完整计数器状态（P 向量和 N 向量）发送给这些邻居
3. 当收到 gossip 消息时，将收到的状态与本地状态合并

**收敛性测量**：
- 在 5 个节点上随机执行 1000 次递增操作
- 测量从最后一次递增到所有 5 个节点达成一致所需的时间
- 预期的收敛时间：几轮 gossip 之内（在 100 毫秒间隔下不到 1 秒）

```json
Request:  {"type": "gossip_status", "msg_id": 1}
Response: {"type": "gossip_status_ok", "in_reply_to": 1, "local_value": 1000, "gossip_rounds": 42, "peers_synced": 4, "convergence_ms": 350}
```

## 涉及概念

- `gossip protocol`
- `counter replication`
- `convergence time`
- `anti-entropy`
- `random peer selection`

## 实现提示

- 每个节点将完整的计数器状态（P 和 N 向量）gossip 给 2 个随机选择的邻居
- Gossip 间隔：每 100 毫秒选择 2 个随机邻居并发送状态
- 收到 gossip 消息时：将收到的状态与本地状态合并
- 在 5 个节点上执行 1000 次递增后，测量所有节点收敛所需的时间
- 收敛的标准是所有节点的 read() 返回相同的值

## 测试用例

### 1. Gossip 复制计数器状态

验证 gossip_status_ok 中 local_value >= 1 且 gossip_rounds >= 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":1}}
{"src":"c1","dest":"n1","body":{"type":"gossip_status","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Gossip 后可以看到远程节点的递增

从 n2 收到 gossip 消息后，读取结果应包含 n2 的递增值。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"n2","dest":"n1","body":{"type":"replicate","msg_id":2,"p_counters":{"n1":0,"n2":10},"n_counters":{"n1":0,"n2":0}}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Gossip Protocols](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/2007PromisesLimitations.pdf)：Demers 等人关于流行病算法在复制数据库维护中的应用

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
