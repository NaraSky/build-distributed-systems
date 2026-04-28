# 分析 CRDT 与乐观并发控制及加锁的权衡

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-4-crdt-tradeoffs>

课程：4. 计数器：分布式状态与 CRDT
任务序号：14
短标题：CRDT 权衡分析
难度：进阶
子主题：更多 CRDT

## 中文导读

这道题让你分析 CRDT、乐观并发控制和加锁三种方案各自的优缺点，并根据不同的使用场景给出推荐。没有万能的方案，每种方法在一致性、可用性和存储开销上都有不同的取舍。这道题帮你建立"因地制宜选方案"的工程思维。

## 题目说明

CRDT 提供了无需协调的最终一致性，但也有代价。将 CRDT 与乐观并发控制（OCC，Optimistic Concurrency Control）和加锁（Locking）进行对比，可以帮助我们理解每种方案各自适用的场景。

**CRDT 的优势**：
- 始终可用（不需要节点间协调）
- 在网络分区下仍然可用（CAP 定理中的 AP 选择）
- 冲突自动解决（无需人工干预）

**CRDT 的劣势**：
- 存储开销大：墓碑、向量时钟、标签等元数据会不断累积
- 合并逻辑复杂：每种数据类型都需要自定义的合并函数
- 一致性较弱：只保证最终一致性（不是线性一致性）

**对比表**：
| 维度 | CRDT | OCC | 加锁 |
|------|------|-----|------|
| 一致性 | 最终一致 | 线性一致 | 线性一致 |
| 可用性 | 始终可用 | 冲突时中止 | 竞争时阻塞 |
| 协调 | 不需要 | 验证阶段 | 获取锁 |
| 存储 | 高（元数据） | 低 | 低 |
| 延迟 | 低（本地操作） | 低（乐观模式） | 不确定（可能等待） |

```json
Request:  {"type": "tradeoff_analysis", "msg_id": 1, "use_case": "shopping_cart", "partition_rate": 0.1, "conflict_rate": 0.3}
Response: {"type": "tradeoff_analysis_ok", "in_reply_to": 1, "recommendation": "CRDT", "reasoning": "High partition rate favors always-available CRDT over blocking approaches"}
```

## 涉及概念

- `CRDT tradeoffs`
- `storage overhead`
- `merge complexity`
- `OCC comparison`
- `coordination-free`

## 实现提示

- CRDT 不需要协调，但墓碑和元数据会增加存储开销
- 加锁提供强一致性，但锁竞争会限制可扩展性
- 乐观并发控制适合低冲突的工作负载，冲突时会中止事务
- CRDT 在网络分区场景下优势明显：无需协调就能保持可用
- 针对三种场景进行对比分析：计数器、购物车、文档协同编辑

## 测试用例

### 1. 高分区率推荐使用 CRDT

高分区率场景应推荐 CRDT。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tradeoff_analysis","msg_id":2,"use_case":"counter","partition_rate":0.5,"conflict_rate":0.1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 低冲突率推荐使用乐观并发控制

低分区率加低冲突率，且需要强一致性时，应推荐乐观并发控制或加锁。

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

- [CRDTs in Practice](https://martin.kleppmann.com/2020/07/06/crdt-hard-parts-hydra.html)：Kleppmann 的演讲，讨论 CRDT 在实践中的难点

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
