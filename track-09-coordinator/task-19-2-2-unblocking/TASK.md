# Show How 3PC Unblocks 2PC Scenarios

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-2-unblocking>

Track: 9. The Coordinator
Task order: 7
Short title: 3PC Unblocking
Difficulty: advanced
Subtrack: Three-Phase Commit (3PC)

## Problem

The key advantage of 3PC over 2PC is that it unblocks one of 2PC's blocking scenarios. When the coordinator crashes after sending `PreCommit`, participants can proceed to commit without waiting for recovery.

**2PC blocking scenario**:
1. Coordinator sends `Prepare` to all participants
2. All participants vote `Yes`
3. Coordinator crashes before sending `Commit`
4. Participants are **blocked**: they don't know if the decision was Commit or Abort
5. Participants must wait for coordinator recovery

**3PC non-blocking scenario**:
1. Coordinator sends `CanCommit` to all participants
2. All participants vote `Yes`
3. Coordinator sends `PreCommit` to all participants
4. All participants acknowledge `PreCommit` and enter `PRE_COMMITTED` state
5. Coordinator crashes before sending `DoCommit`
6. Participants are **not blocked**: they know everyone voted Yes, so they can commit

**Recovery rules for participants in PRE_COMMITTED state**:
```typescript
function onTimeout() {
    if (state === PRE_COMMITTED) {
        // We know everyone voted Yes, so we can commit
        commit();
        broadcast("I have committed");
    }
}
```

**Example test**:
```json
Request:  {"type": "txn_begin", "msg_id": 1, "participants": ["p1", "p2"], "crash_coordinator_after": "pre_commit", "participant_timeout_ms": 2000}
Response: {"type": "txn_begin_ok", "in_reply_to": 1, "txn_id": "txn42"}

// After timeout, participants commit without coordinator:
{"type": "have_committed", "src": "p1", "txn_id": "txn42", "recovery": "timeout"}
{"type": "have_committed", "src": "p2", "txn_id": "txn42", "recovery": "timeout"}
```

## Concepts

- blocking vs non-blocking
- recovery procedures
- timeout handling
- coordinator failure
- participant uncertainty

## Hints

- In 2PC, if coordinator crashes after all vote Yes, participants block forever
- In 3PC, PreCommit phase lets participants know a commit is coming
- If coordinator crashes after PreCommit, participants can commit without waiting
- Participants in PRE_COMMITTED state can timeout and commit unilaterally
- Show this with a test: crash coordinator after PreCommit, verify participants commit

## Test Cases

### 1. 3PC unblocks after PreCommit

Participants should commit after timeout even though coordinator crashed after PreCommit.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"participants":["p1","p2"]}}
{"src":"c1","dest":"coord","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":100,"from":"a","to":"b"}],"crash_coordinator_after":"pre_commit","participant_timeout_ms":2000}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 2PC blocks in same scenario

2PC participants should block (not commit) after timeout because they don't know the decision.

Input:

```json
{"src":"c0","dest":"coord_2pc","body":{"type":"init","msg_id":1,"participants":["p1","p2"],"protocol":"2pc"}}
{"src":"c1","dest":"coord_2pc","body":{"type":"txn_begin","msg_id":2,"participants":["p1","p2"],"operations":[{"transfer":100,"from":"a","to":"b"}],"crash_coordinator_after":"prepare","participant_timeout_ms":2000}}
```

Expected output:

```text
{"src": "coord_2pc", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Non-Blocking Commit Protocols](https://www.cs.princeton.edu/courses/archive/fall05/cos518/papers/skeene.pdf): Paper on non-blocking atomic commitment

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
