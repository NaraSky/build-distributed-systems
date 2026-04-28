# 实现三阶段提交协议

英文标题：Implement Three-Phase Commit Protocol
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-1-three-phase>

课程：9. 协调器：分布式事务
任务序号：6
短标题：Three-Phase Commit
难度：高级
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你完整实现三阶段提交（3PC）协议。与两阶段提交相比，三阶段提交多了一个"预提交"阶段，能在协调者崩溃时减少参与者的阻塞。通过这道题，你将深入理解三阶段提交的协议流程、状态转换以及它如何改善两阶段提交的阻塞问题。

## 题目说明

三阶段提交（3PC）在两阶段提交的基础上增加了一个额外的阶段，以减少阻塞场景。第三个阶段（预提交，PreCommit）确保参与者在协调者崩溃时也能知道提交即将发生。

**协议的三个阶段**：
1. **CanCommit 阶段**：协调者询问所有参与者"你能提交吗？"参与者获取锁并写入预写日志（WAL），然后投票赞成或反对
2. **PreCommit 阶段**：如果所有参与者都投了赞成票，协调者发送 PreCommit。参与者确认并进入"预提交"状态
3. **DoCommit 阶段**：协调者发送 DoCommit。参与者执行变更并发送 HaveCommitted 确认

**状态转换**：
```
参与者状态：
  → INITIAL → CAN_COMMIT? → PRE_COMMITTED → COMMITTED
                  ↓              ↓
                ABORTED        ABORTED
```

**三阶段提交执行示例**：
```json
Request:  {"type": "txn_begin", "msg_id": 1, "participants": ["p1", "p2", "p3"], "operations": [{"transfer": 100, "from": "a", "to": "b"}]}
Response: {"type": "txn_begin_ok", "in_reply_to": 1, "txn_id": "txn42"}

// Phase 1: CanCommit
{"type": "can_commit", "msg_id": 2, "txn_id": "txn42"}
{"type": "can_commit_yes", "in_reply_to": 2, "txn_id": "txn42", "participant": "p1"}
{"type": "can_commit_yes", "in_reply_to": 2, "txn_id": "txn42", "participant": "p2"}
{"type": "can_commit_yes", "in_reply_to": 2, "txn_id": "txn42", "participant": "p3"}

// Phase 2: PreCommit
{"type": "pre_commit", "msg_id": 3, "txn_id": "txn42"}
{"type": "pre_commit_ack", "in_reply_to": 3, "txn_id": "txn42", "participant": "p1"}
{"type": "pre_commit_ack", "in_reply_to": 3, "txn_id": "txn42", "participant": "p2"}
{"type": "pre_commit_ack", "in_reply_to": 3, "txn_id": "txn42", "participant": "p3"}

// Phase 3: DoCommit
{"type": "do_commit", "msg_id": 4, "txn_id": "txn42"}
{"type": "have_committed", "in_reply_to": 4, "txn_id": "txn42", "participant": "p1"}
{"type": "have_committed", "in_reply_to": 4, "txn_id": "txn42", "participant": "p2"}
{"type": "have_committed", "in_reply_to": 4, "txn_id": "txn42", "participant": "p3"}
```

**三阶段提交为什么有效**：
如果协调者在发送 PreCommit 之后崩溃，参与者能确定以下信息：
- 所有参与者都投了赞成票
- 提交即将发生
- 它们可以安全地提交，无需等待协调者恢复

## 涉及概念

- `three-phase commit`
- `CanCommit`
- `PreCommit`
- `DoCommit`
- `non-blocking commit`
- `coordinator recovery`

## 实现提示

- 第一阶段（CanCommit）：协调者询问"你能提交吗？"，参与者投票赞成或反对
- 第二阶段（PreCommit）：如果全部投赞成票，协调者发送 PreCommit，参与者确认
- 第三阶段（DoCommit）：协调者发送 DoCommit，参与者执行提交并确认
- 关键点：PreCommit 让参与者知道提交即将发生，从而支持故障恢复
- 如果协调者在 PreCommit 之后崩溃，参与者可以自行提交而无需等待

## 测试用例

### 1. 成功的三阶段提交事务

txn_begin_ok 应返回事务标识，事务应成功通过所有三个阶段。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":100,"from":"a","to":"b"}]}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 参与者在 CanCommit 阶段投反对票

如果 p2 投了反对票（例如余额不足），协调者应向所有参与者发送 do_abort 中止事务。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":999999,"from":"a","to":"b"}]}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Three-Phase Commit Protocol](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-96-49.pdf)：三阶段提交协议的原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
