# 实现 Three-Phase Commit Protocol

英文标题：Implement Three-Phase Commit Protocol
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-1-three-phase>

课程：9. 协调器：分布式事务
任务序号：6
短标题：Three-Phase Commit
难度：advanced
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你完成 `实现 Three-Phase Commit Protocol`。

重点关注：`three-phase commit`、`CanCommit`、`PreCommit`、`DoCommit`、`non-blocking commit`。

建议先按提示逐步实现：Phase 1 (CanCommit): coordinator asks "Can you commit?" Participants vote Yes/No。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Three-Phase Commit (3PC) adds an extra phase to 2PC to reduce blocking scenarios. The third phase (`PreCommit`) ensures participants know a commit is imminent.

**Protocol phases**:
1. **CanCommit**: Coordinator asks "Can you commit?" Participants acquire locks和write to WAL, then vote Yes/No
2. **PreCommit**: If all voted Yes, coordinator sends `PreCommit`. Participants acknowledge和enter "pre-committed" state
3. **DoCommit**: Coordinator sends `DoCommit`. Participants apply changes和send `HaveCommitted`

**State transitions**:
```
Participant states:
  → INITIAL → CAN_COMMIT? → PRE_COMMITTED → COMMITTED
                  ↓              ↓
                ABORTED        ABORTED
```

**Example 3PC execution**:
```JSON
请求:  {"type": "txn_begin", "msg_id": 1, "participants": ["p1", "p2", "p3"], "operations": [{"transfer": 100, "from": "a", "to": "b"}]}
响应: {"type": "txn_begin_ok", "in_reply_to": 1, "txn_id": "txn42"}

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

**Why 3PC helps**:
If coordinator crashes after `PreCommit`, participants know:
- All participants voted Yes
- A commit is imminent
- They can safely commit without waiting用于recovery

## 涉及概念

- `three-phase commit`
- `CanCommit`
- `PreCommit`
- `DoCommit`
- `non-blocking commit`
- `coordinator recovery`

## 实现提示

- Phase 1 (CanCommit): coordinator asks "Can you commit?" Participants vote Yes/No
- Phase 2 (PreCommit): coordinator sends PreCommit if all voted Yes. Participants acknowledge
- Phase 3 (DoCommit): coordinator sends DoCommit. Participants commit和acknowledge
- The key: PreCommit lets participants know a commit is coming, enabling recovery
- If coordinator crashes after PreCommit, participants can commit without waiting

## 测试用例

### 1. Successful 3PC 事务

txn_begin_ok should return txn_id和the 事务 should complete through all 3 phases.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":100,"from":"a","to":"b"}]}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Participant votes No in CanCommit

If p2 votes No (insufficient funds), coordinator should send do_abort to all participants.

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

- [Three-Phase Commit Protocol](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-96-49.pdf)：Original paper on 3PC

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
