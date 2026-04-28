# Show 3PC Blocking Under Network Partition

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-3-network-partition>

Track: 9. The Coordinator
Task order: 8
Short title: 3PC Network Partition
Difficulty: advanced
Subtrack: Three-Phase Commit (3PC)

## Problem

While 3PC improves on 2PC, it still has blocking scenarios. The key limitation: if a network partition occurs before `PreCommit`, participants may not be able to proceed.

**Scenario 1: Partition before PreCommit**:
1. Coordinator sends `CanCommit` to all participants
2. Some participants vote `Yes`, others are partitioned
3. Coordinator cannot collect all votes
4. **No participant can proceed**: non-partitioned participants don't know if all voted Yes
5. **Result**: blocking

**Scenario 2: Partition during PreCommit**:
1. Coordinator sends `CanCommit`, all participants vote `Yes`
2. Network partition occurs
3. Coordinator sends `PreCommit` to only some participants
4. Partitioned participants never receive `PreCommit`
5. **Result**: partitioned participants block, non-partitioned participants can timeout and commit

**Example: Partition before PreCommit**:
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

**Why this is unavoidable**:
- Before `PreCommit`, participants don't know if all participants voted Yes
- If any participant voted No, the transaction must abort
- Without knowing all votes, no participant can safely decide
- This is a fundamental trade-off: 3PC reduces but doesn't eliminate blocking

## Concepts

- network partition
- blocking scenarios
- split brain
- safety vs liveness
- CAP theorem

## Hints

- 3PC still blocks if coordinator crashes before PreCommit
- 3PC blocks if network partition separates coordinator from some participants
- If participants are in CAN_COMMIT state and can't reach coordinator, they must wait
- Show: partition coordinator from participants after CanCommit phase
- Result: non-partitioned participants block because they don't know if all voted Yes

## Test Cases

### 1. Partition before PreCommit blocks

p1 and p2 should block (not commit) because they don't know if p3 voted Yes or No.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2","p3"],"operations":[{"transfer":100,"from":"a","to":"b"}],"partition_after":"can_commit","partitioned_participants":["p3"],"timeout_ms":2000}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Partition during PreCommit allows commit

p1 and p2 should commit after timeout because they received PreCommit and know all voted Yes.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2","p3"],"operations":[{"transfer":100,"from":"a","to":"b"}],"partition_after":"pre_commit","partitioned_participants":["p3"],"timeout_ms":2000}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [CAP Theorem and Commit Protocols](https://www.ibm.com/topics/cap-theorem): How CAP theorem relates to distributed commit protocols

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
