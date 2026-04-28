# Gossip PN-计数器 Across a Cluster

英文标题：Gossip PN-Counter Across a Cluster
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-4-gossip-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：9
短标题：Gossip 计数器
难度：advanced
子主题：G-计数器和PN-计数器

## 中文导读

本题要求你完成 `Gossip PN-计数器 Across a Cluster`。

重点关注：`gossip protocol`、`counter replication`、`convergence time`、`anti-entropy`、`random peer selection`。

建议先按提示逐步实现：Each 节点 gossips its full 计数器 state (P和N vectors) to 2 random peers。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

To replicate the PN-计数器 across a 集群, each 节点 periodically gossips its full state to random peers. This is an anti-entropy protocol that guarantees eventual convergence.

**gossip protocol**:
1. Every 100ms, select 2 random peers from the 节点 list
2. Send your full 计数器 state (P vector + N vector) to those peers
3. When you receive a gossip 消息, merge the received state，包含your local state

**Convergence measurement**:
- Apply 1000 random increments across 5 节点
- Measure the time from the last increment until all 5 节点 agree on the value
- Expected convergence: within a few gossip rounds (< 1 second，包含100ms interval)

```JSON
请求:  {"type": "gossip_status", "msg_id": 1}
响应: {"type": "gossip_status_ok", "in_reply_to": 1, "local_value": 1000, "gossip_rounds": 42, "peers_synced": 4, "convergence_ms": 350}
```

## 涉及概念

- `gossip protocol`
- `counter replication`
- `convergence time`
- `anti-entropy`
- `random peer selection`

## 实现提示

- Each 节点 gossips its full 计数器 state (P和N vectors) to 2 random peers
- gossip interval: every 100ms, select 2 random peers和send your state
- On receiving gossip: merge the received state，包含your local state
- After 1000 increments across 5 节点, measure time until all 节点 converge
- Convergence = all 节点 report the same value用于read()

## 测试用例

### 1. Gossip replicates 计数器 state

gossip_status_ok should show local_value >= 1和gossip_rounds >= 0.

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

### 2. Remote increments are visible after Gossip

After receiving gossip from n2, read should include n2 increments.

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

- [Gossip Protocols](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/2007PromisesLimitations.pdf)：Demers et al. - Epidemic algorithms用于replicated database maintenance

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
