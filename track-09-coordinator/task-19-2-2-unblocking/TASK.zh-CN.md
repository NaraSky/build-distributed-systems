# Show How 3PC Unblocks 2PC Scenarios

英文标题：Show How 3PC Unblocks 2PC Scenarios
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-2-unblocking>

课程：9. 协调器：分布式事务
任务序号：7
短标题：3PC Unblocking
难度：advanced
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你完成 `Show How 3PC Unblocks 2PC Scenarios`。

重点关注：`blocking vs non-blocking`、`recovery procedures`、`timeout handling`、`coordinator failure`、`participant uncertainty`。

建议先按提示逐步实现：In 2PC, if coordinator crashes after all vote Yes, participants block forever。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The key advantage of 3PC over 2PC is that it unblocks one of 2PC's blocking scenarios. When the coordinator crashes after sending `PreCommit`, participants can proceed to commit without waiting用于recovery.

**2PC blocking scenario**:
1. Coordinator sends `Prepare` to all participants
2. All participants vote `Yes`
3. Coordinator crashes before sending `Commit`
4. Participants are **blocked**: they don't know if the decision was Commit or Abort
5. Participants must wait用于coordinator recovery

**3PC non-blocking scenario**:
1. Coordinator sends `CanCommit` to all participants
2. All participants vote `Yes`
3. Coordinator sends `PreCommit` to all participants
4. All participants acknowledge `PreCommit`和enter `PRE_COMMITTED` state
5. Coordinator crashes before sending `DoCommit`
6. Participants are **not blocked**: they know everyone voted Yes, so they can commit

**Recovery rules用于participants in PRE_COMMITTED state**:
```typescript
function onTimeout() {
    if (state === PRE_COMMITTED) {
        // We know everyone voted Yes, so we can commit
        commit();
        广播("I have committed");
    }
}
```

**Example test**:
```JSON
请求:  {"type": "txn_begin", "msg_id": 1, "participants": ["p1", "p2"], "crash_coordinator_after": "pre_commit", "participant_timeout_ms": 2000}
响应: {"type": "txn_begin_ok", "in_reply_to": 1, "txn_id": "txn42"}

// After 超时, participants commit without coordinator:
{"type": "have_committed", "src": "p1", "txn_id": "txn42", "recovery": "超时"}
{"type": "have_committed", "src": "p2", "txn_id": "txn42", "recovery": "超时"}
```

## 涉及概念

- `blocking vs non-blocking`
- `recovery procedures`
- `timeout handling`
- `coordinator failure`
- `participant uncertainty`

## 实现提示

- In 2PC, if coordinator crashes after all vote Yes, participants block forever
- In 3PC, PreCommit phase lets participants know a commit is coming
- If coordinator crashes after PreCommit, participants can commit without waiting
- Participants in PRE_COMMITTED state can 超时和commit unilaterally
- Show this，包含a test: crash coordinator after PreCommit, verify participants commit

## 测试用例

### 1. 3PC unblocks after PreCommit

Participants should commit after 超时 even though coordinator crashed after PreCommit.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":100,"from":"a","to":"b"}],"crash_coordinator_after":"pre_commit","participant_timeout_ms":2000}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 2PC blocks in same scenario

2PC participants should block (not commit) after 超时 because they don't know the decision.

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

- [Non-Blocking Commit Protocols](https://www.cs.princeton.edu/courses/archive/fall05/cos518/papers/skeene.pdf)：Paper on non-blocking atomic commitment

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
