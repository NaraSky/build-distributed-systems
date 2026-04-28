# Implement Three-Phase Commit Protocol

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-1-three-phase>

Track: 9. The Coordinator
Task order: 6
Short title: Three-Phase Commit
Difficulty: advanced
Subtrack: Three-Phase Commit (3PC)

## Problem

Three-Phase Commit (3PC) adds an extra phase to 2PC to reduce blocking scenarios. The third phase (`PreCommit`) ensures participants know a commit is imminent.

**Protocol phases**:
1. **CanCommit**: Coordinator asks "Can you commit?" Participants acquire locks and write to WAL, then vote Yes/No
2. **PreCommit**: If all voted Yes, coordinator sends `PreCommit`. Participants acknowledge and enter "pre-committed" state
3. **DoCommit**: Coordinator sends `DoCommit`. Participants apply changes and send `HaveCommitted`

**State transitions**:
```
Participant states:
  → INITIAL → CAN_COMMIT? → PRE_COMMITTED → COMMITTED
                  ↓              ↓
                ABORTED        ABORTED
```

**Example 3PC execution**:
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

**Why 3PC helps**:
If coordinator crashes after `PreCommit`, participants know:
- All participants voted Yes
- A commit is imminent
- They can safely commit without waiting for recovery

## Concepts

- three-phase commit
- CanCommit
- PreCommit
- DoCommit
- non-blocking commit
- coordinator recovery

## Hints

- Phase 1 (CanCommit): coordinator asks "Can you commit?" Participants vote Yes/No
- Phase 2 (PreCommit): coordinator sends PreCommit if all voted Yes. Participants acknowledge
- Phase 3 (DoCommit): coordinator sends DoCommit. Participants commit and acknowledge
- The key: PreCommit lets participants know a commit is coming, enabling recovery
- If coordinator crashes after PreCommit, participants can commit without waiting

## Test Cases

### 1. Successful 3PC transaction

txn_begin_ok should return txn_id and the transaction should complete through all 3 phases.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":100,"from":"a","to":"b"}]}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Participant votes No in CanCommit

If p2 votes No (insufficient funds), coordinator should send do_abort to all participants.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":999999,"from":"a","to":"b"}]}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Three-Phase Commit Protocol](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-96-49.pdf): Original paper on 3PC

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
