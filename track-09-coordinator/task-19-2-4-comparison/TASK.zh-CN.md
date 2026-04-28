# Compare 2PC vs 3PC Protocols

英文标题：Compare 2PC vs 3PC Protocols
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-4-comparison>

课程：9. 协调器：分布式事务
任务序号：9
短标题：2PC vs 3PC Comparison
难度：intermediate
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你完成 `Compare 2PC vs 3PC Protocols`。

重点关注：`protocol comparison`、`message complexity`、`blocking scenarios`、`real-world usage`、`performance trade-offs`。

建议先按提示逐步实现：2PC: 2 rounds (Prepare + Commit/Abort), 3PC: 3 rounds (CanCommit + PreCommit + DoCommit)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Understanding the trade-offs between 2PC和3PC helps choose the right protocol用于your use case.

**消息 complexity**:
```
2PC (happy path):
  Prepare → 2N 消息 (N requests, N replies)
  Commit  → 2N 消息 (N requests, N replies)
  Total: 4N 消息

3PC (happy path):
  CanCommit → 2N 消息
  PreCommit  → 2N 消息
  DoCommit   → 2N 消息
  Total: 6N 消息
```

**Blocking scenarios**:
```
2PC blocks when:
  - Coordinator crashes after collecting all Yes votes
  - Participant crashes after voting Yes but before receiving decision

3PC blocks when:
  - Coordinator crashes before sending PreCommit
  - 网络 partition separates coordinator from participants before PreCommit
  - (Does NOT block if coordinator crashes after PreCommit)
```

**Real-world usage**:
- **2PC**: Widely used (XA transactions, databases, 消息 queues)
- **3PC**: Rarely used due to complexity和remaining blocking scenarios
- **共识-based**: Paxos/Raft are preferred用于non-blocking commit

**Performance comparison**:
```JSON
请求:  {"type": "benchmark", "msg_id": 1, "protocols": ["2pc", "3pc"], "participants": 5, "transactions": 100}
响应: {"type": "benchmark_ok", "in_reply_to": 1, "results": {"2pc": {"avg_latency_ms": 45, "throughput_tps": 2200}, "3pc": {"avg_latency_ms": 68, "throughput_tps": 1450}}}
```

**When to use each**:
- **Use 2PC**: Simple, widely supported, acceptable blocking risk
- **Use 3PC**: Need slightly better availability, can tolerate extra complexity
- **Use 共识**: Need true non-blocking commit, can tolerate higher latency

## 涉及概念

- `protocol comparison`
- `message complexity`
- `blocking scenarios`
- `real-world usage`
- `performance trade-offs`

## 实现提示

- 2PC: 2 rounds (Prepare + Commit/Abort), 3PC: 3 rounds (CanCommit + PreCommit + DoCommit)
- 2PC blocks if coordinator crashes after Prepare, 3PC blocks if coordinator crashes before PreCommit
- 3PC reduces but doesn't eliminate blocking
- 3PC is rarely used in practice due to complexity和remaining blocking scenarios
- Most systems use 2PC or 共识-based approaches (Paxos/Raft)

## 测试用例

### 1. 基准测试 2PC vs 3PC 延迟

benchmark_ok should show 2PC has lower latency than 3PC due to fewer 消息 rounds.

输入：

```json
{"src":"c0","dest":"benchmarker","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"benchmarker","body":{"type":"benchmark","msg_id":2,"protocols":["2pc","3pc"],"participants":3,"transactions":100}}
```

期望输出：

```text
{"src": "benchmarker", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compare blocking scenarios

compare_blocking_ok should return a table showing 2PC has 2 blocking scenarios, 3PC has 1.

输入：

```json
{"src":"c0","dest":"comparator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"comparator","body":{"type":"compare_blocking","msg_id":2,"protocols":["2pc","3pc"]}}
```

期望输出：

```text
{"src": "comparator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Two-Phase Commit vs Three-Phase Commit](https://martin.kleppmann.com/2018/09/24/two-phase-commit.html)：Blog post comparing 2PC和3PC by Martin Kleppmann

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
