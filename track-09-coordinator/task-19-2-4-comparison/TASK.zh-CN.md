# 对比两阶段提交与三阶段提交

英文标题：Compare 2PC vs 3PC Protocols
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-4-comparison>

课程：9. 协调器：分布式事务
任务序号：9
短标题：2PC vs 3PC Comparison
难度：进阶
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你对比两阶段提交和三阶段提交的优劣，包括消息复杂度、阻塞场景和实际应用情况。理解这些取舍有助于你在实际系统中选择合适的分布式事务协议。

## 题目说明

理解两阶段提交和三阶段提交之间的取舍，有助于为你的应用场景选择正确的协议。

**消息复杂度**：
```
2PC（正常路径）：
  Prepare → 2N 条消息（N 条请求，N 条回复）
  Commit  → 2N 条消息（N 条请求，N 条回复）
  总计：4N 条消息

3PC（正常路径）：
  CanCommit → 2N 条消息
  PreCommit → 2N 条消息
  DoCommit  → 2N 条消息
  总计：6N 条消息
```

**阻塞场景对比**：
```
2PC 会阻塞的情况：
  - 协调者在收集到所有赞成票后崩溃
  - 参与者在投赞成票后、收到决策之前崩溃

3PC 会阻塞的情况：
  - 协调者在发送 PreCommit 之前崩溃
  - 网络分区在 PreCommit 之前将协调者与参与者隔开
  - （如果协调者在 PreCommit 之后崩溃，不会阻塞）
```

**实际应用情况**：
- **两阶段提交**：广泛使用（XA 事务、数据库、消息队列）
- **三阶段提交**：由于复杂度高且仍存在阻塞场景，很少在实际中使用
- **基于共识的方案**：Paxos 和 Raft 是实现非阻塞提交的首选

**性能对比**：
```json
Request:  {"type": "benchmark", "msg_id": 1, "protocols": ["2pc", "3pc"], "participants": 5, "transactions": 100}
Response: {"type": "benchmark_ok", "in_reply_to": 1, "results": {"2pc": {"avg_latency_ms": 45, "throughput_tps": 2200}, "3pc": {"avg_latency_ms": 68, "throughput_tps": 1450}}}
```

**何时使用哪种协议**：
- **使用两阶段提交**：实现简单、广泛支持、可以接受阻塞风险
- **使用三阶段提交**：需要稍好的可用性、能承受额外的复杂度
- **使用共识算法**：需要真正的非阻塞提交、能容忍更高的延迟

## 涉及概念

- `protocol comparison`
- `message complexity`
- `blocking scenarios`
- `real-world usage`
- `performance trade-offs`

## 实现提示

- 两阶段提交有两轮交互（Prepare + Commit/Abort），三阶段提交有三轮交互（CanCommit + PreCommit + DoCommit）
- 两阶段提交在协调者于 Prepare 之后崩溃时阻塞，三阶段提交在协调者于 PreCommit 之前崩溃时阻塞
- 三阶段提交减少了阻塞，但并未完全消除
- 三阶段提交在实际中很少使用，因为复杂度高且仍存在阻塞场景
- 大多数系统使用两阶段提交或基于共识的方案（Paxos/Raft）

## 测试用例

### 1. 两阶段提交与三阶段提交的延迟基准测试

benchmark_ok 应显示两阶段提交的延迟低于三阶段提交，因为消息轮次更少。

输入：

```json
{"src":"c0","dest":"benchmarker","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"benchmarker","body":{"type":"benchmark","msg_id":2,"protocols":["2pc","3pc"],"participants":3,"transactions":100}}
```

期望输出：

```text
{"src": "benchmarker", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 对比阻塞场景

compare_blocking_ok 应返回一个对比表，显示两阶段提交有两个阻塞场景，三阶段提交有一个。

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

- [Two-Phase Commit vs Three-Phase Commit](https://martin.kleppmann.com/2018/09/24/two-phase-commit.html)：Martin Kleppmann 撰写的两阶段提交与三阶段提交对比博文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
