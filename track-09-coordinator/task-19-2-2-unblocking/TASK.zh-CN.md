# 展示三阶段提交如何解除两阶段提交的阻塞

英文标题：Show How 3PC Unblocks 2PC Scenarios
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-2-unblocking>

课程：9. 协调器：分布式事务
任务序号：7
短标题：3PC Unblocking
难度：高级
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你通过对比实验，展示三阶段提交相比两阶段提交的核心优势：当协调者在 PreCommit 之后崩溃时，参与者可以自行提交而不会被永久阻塞。这道题帮助你直观理解阻塞与非阻塞协议的关键区别。

## 题目说明

三阶段提交相比两阶段提交的核心优势在于：它能解除两阶段提交中的一种阻塞场景。当协调者在发送 PreCommit 之后崩溃时，参与者可以继续完成提交，而不需要等待协调者恢复。

**两阶段提交的阻塞场景**：
1. 协调者向所有参与者发送 Prepare
2. 所有参与者投赞成票
3. 协调者在发送 Commit 之前崩溃
4. 参与者被**阻塞**：它们不知道最终决策是提交还是中止
5. 参与者只能等待协调者恢复

**三阶段提交的非阻塞场景**：
1. 协调者向所有参与者发送 CanCommit
2. 所有参与者投赞成票
3. 协调者向所有参与者发送 PreCommit
4. 所有参与者确认 PreCommit 并进入 PRE_COMMITTED 状态
5. 协调者在发送 DoCommit 之前崩溃
6. 参与者**不会被阻塞**：它们知道所有人都投了赞成票，因此可以安全提交

**处于 PRE_COMMITTED 状态的参与者的恢复规则**：
```typescript
function onTimeout() {
    if (state === PRE_COMMITTED) {
        // We know everyone voted Yes, so we can commit
        commit();
        broadcast("I have committed");
    }
}
```

**测试示例**：
```json
Request:  {"type": "txn_begin", "msg_id": 1, "participants": ["p1", "p2"], "crash_coordinator_after": "pre_commit", "participant_timeout_ms": 2000}
Response: {"type": "txn_begin_ok", "in_reply_to": 1, "txn_id": "txn42"}

// After timeout, participants commit without coordinator:
{"type": "have_committed", "src": "p1", "txn_id": "txn42", "recovery": "timeout"}
{"type": "have_committed", "src": "p2", "txn_id": "txn42", "recovery": "timeout"}
```

## 涉及概念

- `blocking vs non-blocking`
- `recovery procedures`
- `timeout handling`
- `coordinator failure`
- `participant uncertainty`

## 实现提示

- 在两阶段提交中，如果协调者在所有人投赞成票后崩溃，参与者会永久阻塞
- 在三阶段提交中，PreCommit 阶段让参与者知道提交即将发生
- 如果协调者在 PreCommit 之后崩溃，参与者可以自行提交而无需等待
- 处于 PRE_COMMITTED 状态的参与者可以在超时后单方面提交
- 通过测试来验证：让协调者在 PreCommit 之后崩溃，确认参与者能自行完成提交

## 测试用例

### 1. 三阶段提交在 PreCommit 之后解除阻塞

即使协调者在 PreCommit 之后崩溃，参与者也应该在超时后成功提交。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":100,"from":"a","to":"b"}],"crash_coordinator_after":"pre_commit","participant_timeout_ms":2000}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 两阶段提交在同一场景下阻塞

两阶段提交的参与者在超时后应该保持阻塞（不提交），因为它们不知道最终决策。

输入：

```json
{"src":"c0","dest":"coord_2pc","body":{"type":"init","msg_id":1,"participants":["p1","p2"],"protocol":"2pc"}}
{"src":"c1","dest":"coord_2pc","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":100,"from":"a","to":"b"}],"crash_coordinator_after":"prepare","participant_timeout_ms":2000}}
```

期望输出：

```text
{"src": "coord_2pc", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Non-Blocking Commit Protocols](https://www.cs.princeton.edu/courses/archive/fall05/cos518/papers/skeene.pdf)：关于非阻塞原子提交的论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
