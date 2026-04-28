# 展示三阶段提交在网络分区下的阻塞

英文标题：Show 3PC Blocking Under Network Partition
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-3-network-partition>

课程：9. 协调器：分布式事务
任务序号：8
短标题：3PC Network Partition
难度：高级
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你展示三阶段提交在网络分区情况下仍然会出现阻塞。虽然三阶段提交改进了两阶段提交，但它并不能解决所有阻塞问题。通过这道题，你将理解分布式提交协议的根本局限性，以及安全性与活性之间的取舍。

## 题目说明

虽然三阶段提交改进了两阶段提交，但它仍然存在阻塞场景。关键的局限是：如果在 PreCommit 之前发生网络分区（Network Partition），参与者可能无法继续推进事务。

**场景一：PreCommit 之前发生分区**：
1. 协调者向所有参与者发送 CanCommit
2. 部分参与者投赞成票，其他参与者被分区隔离
3. 协调者无法收集到所有投票
4. **没有参与者能继续推进**：未被隔离的参与者不知道所有人是否都投了赞成票
5. **结果**：阻塞

**场景二：PreCommit 期间发生分区**：
1. 协调者发送 CanCommit，所有参与者投赞成票
2. 发生网络分区
3. 协调者只能将 PreCommit 发送给部分参与者
4. 被隔离的参与者永远收不到 PreCommit
5. **结果**：被隔离的参与者阻塞，未被隔离的参与者可以超时后提交

**示例：PreCommit 之前发生分区**：
```json
Request:  {"type": "txn_begin", "msg_id": 1, "participants": ["p1", "p2", "p3"], "partition_after": "can_commit", "partitioned_participants": ["p3"]}
Response: {"type": "txn_begin_ok", "in_reply_to": 1, "txn_id": "txn42"}

// p1 and p2 vote Yes
{"type": "can_commit_yes", "src": "p1", "txn_id": "txn42"}
{"type": "can_commit_yes", "src": "p2", "txn_id": "txn42"}

// p3 is partitioned, cannot vote
// Coordinator cannot proceed: doesn't know if p3 would vote Yes or No
// p1 and p2 block: they don't know if p3 voted No
```

**为什么这是不可避免的**：
- 在 PreCommit 之前，参与者不知道是否所有人都投了赞成票
- 如果有任何参与者投了反对票，事务必须中止
- 在不知道所有投票结果的情况下，没有参与者能安全地做出决策
- 这是一个根本性的取舍：三阶段提交减少了阻塞，但无法完全消除

## 涉及概念

- `network partition`
- `blocking scenarios`
- `split brain`
- `safety vs liveness`
- `CAP theorem`

## 实现提示

- 如果协调者在 PreCommit 之前崩溃，三阶段提交仍然会阻塞
- 如果网络分区将协调者与部分参与者隔开，三阶段提交也会阻塞
- 如果参与者处于 CAN_COMMIT 状态且无法联系协调者，它们只能等待
- 演示：在 CanCommit 阶段之后将协调者与参与者隔开
- 结果：未被隔离的参与者会阻塞，因为它们不知道所有人是否都投了赞成票

## 测试用例

### 1. PreCommit 之前发生分区导致阻塞

p1 和 p2 应该阻塞（不提交），因为它们不知道 p3 投的是赞成票还是反对票。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2","p3"],"operations":[{"transfer":100,"from":"a","to":"b"}],"partition_after":"can_commit","partitioned_participants":["p3"],"timeout_ms":2000}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. PreCommit 期间发生分区允许提交

p1 和 p2 应该在超时后提交，因为它们已经收到了 PreCommit，知道所有人都投了赞成票。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2","p3"],"operations":[{"transfer":100,"from":"a","to":"b"}],"partition_after":"pre_commit","partitioned_participants":["p3"],"timeout_ms":2000}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [CAP Theorem and Commit Protocols](https://www.ibm.com/topics/cap-theorem)：CAP 定理与分布式提交协议的关系

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
