# Show 3PC Blocking Under Network Partition

英文标题：Show 3PC Blocking Under Network Partition
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-3-network-partition>

课程：9. 协调器：分布式事务
任务序号：8
短标题：3PC Network Partition
难度：advanced
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你完成 `Show 3PC Blocking Under Network Partition`。

重点关注：`network partition`、`blocking scenarios`、`split brain`、`safety vs liveness`、`CAP theorem`。

建议先按提示逐步实现：3PC still blocks if coordinator crashes before PreCommit。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

While 3PC improves on 2PC, it still has blocking scenarios. The key limitation: if a 网络 partition occurs before `PreCommit`, participants may not be able to proceed.

**Scenario 1: Partition before PreCommit**:
1. Coordinator sends `CanCommit` to all participants
2. Some participants vote `Yes`, others are partitioned
3. Coordinator cannot collect all votes
4. **No participant can proceed**: non-partitioned participants don't know if all voted Yes
5. **Result**: blocking

**Scenario 2: Partition during PreCommit**:
1. Coordinator sends `CanCommit`, all participants vote `Yes`
2. 网络 partition occurs
3. Coordinator sends `PreCommit` to only some participants
4. Partitioned participants never receive `PreCommit`
5. **Result**: partitioned participants block, non-partitioned participants can 超时和commit

**Example: Partition before PreCommit**:
```JSON
请求:  {"type": "txn_begin", "msg_id": 1, "participants": ["p1", "p2", "p3"], "partition_after": "can_commit", "partitioned_participants": ["p3"]}
响应: {"type": "txn_begin_ok", "in_reply_to": 1, "txn_id": "txn42"}

// p1和p2 vote Yes
{"type": "can_commit_yes", "src": "p1", "txn_id": "txn42"}
{"type": "can_commit_yes", "src": "p2", "txn_id": "txn42"}

// p3 is partitioned, cannot vote
// Coordinator cannot proceed: doesn't know if p3 would vote Yes or No
// p1和p2 block: they don't know if p3 voted No
```

**Why this is unavoidable**:
- Before `PreCommit`, participants don't know if all participants voted Yes
- If any participant voted No, the 事务 must abort
- Without knowing all votes, no participant can safely decide
- This is a fundamental trade-off: 3PC reduces but doesn't eliminate blocking

## 涉及概念

- `network partition`
- `blocking scenarios`
- `split brain`
- `safety vs liveness`
- `CAP theorem`

## 实现提示

- 3PC still blocks if coordinator crashes before PreCommit
- 3PC blocks if 网络 partition separates coordinator from some participants
- If participants are in CAN_COMMIT state和can't reach coordinator, they must wait
- Show: partition coordinator from participants after CanCommit phase
- Result: non-partitioned participants block because they don't know if all voted Yes

## 测试用例

### 1. Partition before PreCommit blocks

p1和p2 should block (not commit) because they don't know if p3 voted Yes or No.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2","p3"],"operations":[{"transfer":100,"from":"a","to":"b"}],"partition_after":"can_commit","partitioned_participants":["p3"],"timeout_ms":2000}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Partition during PreCommit allows commit

p1和p2 should commit after 超时 because they received PreCommit和know all voted Yes.

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

- [CAP Theorem和Commit Protocols](https://www.ibm.com/topics/cap-theorem)：How CAP theorem relates to distributed commit protocols

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
