# Analyze CRDT Tradeoffs vs. OCC和Locking

英文标题：Analyze CRDT Tradeoffs vs. OCC和Locking
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-4-crdt-tradeoffs>

课程：4. 计数器：分布式状态与 CRDT
任务序号：14
短标题：CRDT Tradeoffs
难度：intermediate
子主题：More CRDTs

## 中文导读

本题要求你完成 `Analyze CRDT Tradeoffs vs. OCC和Locking`。

重点关注：`CRDT tradeoffs`、`storage overhead`、`merge complexity`、`OCC comparison`、`coordination-free`。

建议先按提示逐步实现：CRDTs: no coordination, but tombstones和元数据 increase 存储 cost。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

CRDTs provide coordination-free 最终一致性, but come，包含tradeoffs. Comparing CRDTs，包含OCC (Optimistic Concurrency Control)和locking reveals when each approach is appropriate.

**CRDT advantages**:
- Always available (no coordination required)
- Works under 网络 partitions (AP in CAP)
- Automatic conflict resolution (no human intervention)

**CRDT disadvantages**:
- 存储 overhead: tombstones, vector clocks, tags accumulate
- Merge complexity: custom merge functions用于each data type
- Weaker consistency: only eventual (not 线性一致)

**Comparison table**:
| Aspect | CRDT | OCC | Locking |
|--------|------|-----|---------|
| Consistency | Eventual | 线性一致 | 线性一致 |
| Availability | Always | Abort on conflict | Block on contention |
| Coordination | None | Validation phase | Lock acquisition |
| 存储 | High (元数据) | Low | Low |
| Latency | Low (local) | Low (optimistic) | Variable (wait) |

```JSON
请求:  {"type": "tradeoff_analysis", "msg_id": 1, "use_case": "shopping_cart", "partition_rate": 0.1, "conflict_rate": 0.3}
响应: {"type": "tradeoff_analysis_ok", "in_reply_to": 1, "recommendation": "CRDT", "reasoning": "High partition rate favors always-available CRDT over blocking approaches"}
```

## 涉及概念

- `CRDT tradeoffs`
- `storage overhead`
- `merge complexity`
- `OCC comparison`
- `coordination-free`

## 实现提示

- CRDTs: no coordination, but tombstones和元数据 increase 存储 cost
- Locking: strong consistency, but lock contention limits scalability
- OCC (Optimistic Concurrency Control): good用于low-conflict workloads, aborts on conflict
- CRDTs shine under partition: they remain available without coordination
- Build a comparison用于3 use cases: 计数器, shopping cart, document editing

## 测试用例

### 1. High partition rate recommends CRDT

High partition rate should recommend CRDT.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tradeoff_analysis","msg_id":2,"use_case":"counter","partition_rate":0.5,"conflict_rate":0.1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Low conflict rate recommends OCC

Low partition + low conflict，包含strong consistency need should recommend OCC or Locking.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tradeoff_analysis","msg_id":2,"use_case":"banking","partition_rate":0.01,"conflict_rate":0.05}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [CRDTs in Practice](https://martin.kleppmann.com/2020/07/06/crdt-hard-parts-hydra.html)：Kleppmann - CRDTs: The Hard Parts

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
