# Implement the Raft Commitment Rule

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-1-commit-rule>

Track: 6. The Consensus
Task order: 6
Short title: Commit Rule
Difficulty: intermediate
Subtrack: Commitment and Application

## Problem

Implement the Raft commitment rule: an entry is committed when a majority of nodes have it in their log. The leader uses `matchIndex[]` to determine when this is true.

```json
Request:  {"type": "check_commit", "msg_id": 1, "log_length": 5, "match_indices": {"n1": 5, "n2": 5, "n3": 3, "n4": 2, "n5": 1}, "current_term": 3}
Response: {"type": "check_commit_ok", "in_reply_to": 1, "new_commit_index": 5, "majority_count": 2, "quorum": 3, "committed": true}

Request:  {"type": "advance_commit", "msg_id": 2, "old_commit_index": 3, "match_indices": {"n1": 7, "n2": 5, "n3": 5, "n4": 3, "n5": 2}, "current_term": 3}
Response: {"type": "advance_commit_ok", "in_reply_to": 2, "new_commit_index": 5, "entries_committed": 2}
```

## Concepts

- commitment
- majority replication
- commitIndex
- log replication

## Hints

- An entry is committed when a majority of nodes have it in their log
- The leader tracks matchIndex[] for each follower
- commitIndex advances when a majority of matchIndex values >= a given index
- Only entries from the current term can directly advance commitIndex
- Entries from previous terms are committed indirectly

## Test Cases

### 1. Majority replication commits entry

check_commit_ok should show new_commit_index: 3 since n1 and n2 (majority of 3) have index 3.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"check_commit","msg_id":2,"log_length":3,"match_indices":{"n1":3,"n2":3,"n3":1},"current_term":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. No majority means no commit advance

Only 2 out of 5 have index 5. Quorum needs 3. committed: false.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4","n5"]}}
{"src":"c1","dest":"n1","body":{"type":"check_commit","msg_id":2,"log_length":5,"match_indices":{"n1":5,"n2":5,"n3":1,"n4":1,"n5":1},"current_term":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Raft Consensus - Log Commitment](https://raft.github.io/raft.pdf): Raft paper Section 5.3-5.4 on commitment rules

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
