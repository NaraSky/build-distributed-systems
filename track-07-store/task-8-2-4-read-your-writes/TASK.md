# Guarantee Read-Your-Writes with Follower Reads

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-4-read-your-writes>

Track: 7. The Store
Task order: 9
Short title: Read-Your-Writes
Difficulty: advanced
Subtrack: Read Optimization

## Problem

Ensure read-your-writes consistency even when using follower reads. Clients send their `last_write_index` with each read. Followers only serve if they have applied that index.

```json
Request:  {"type": "write", "msg_id": 1, "key": "x", "value": "new"}
Response: {"type": "write_ok", "in_reply_to": 1, "commit_index": 10}

Request:  {"type": "ryw_read", "msg_id": 2, "key": "x", "last_write_index": 10, "prefer_follower": true}
Response: {"type": "ryw_read_ok", "in_reply_to": 2, "value": "new", "served_by": "n2", "follower_applied_index": 10, "waited_ms": 50}

Request:  {"type": "ryw_read", "msg_id": 3, "key": "x", "last_write_index": 15, "prefer_follower": true}
Response: {"type": "ryw_read_ok", "in_reply_to": 3, "value": "new", "served_by": "n1", "reason": "follower_behind_redirected_to_leader"}
```

## Concepts

- read-your-writes
- session consistency
- commit index tracking
- client token

## Hints

- Clients send their last-seen commit_index with each read request
- Followers only serve the read if they have applied at least that index
- If the follower is behind, it either waits or redirects to the leader
- This combines the scalability of follower reads with read-your-writes guarantee
- The client tracks the commit_index from write responses

## Test Cases

### 1. Read-your-writes from follower

ryw_read_ok should show the read was served with follower_applied_index >= 5.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ryw_read","msg_id":2,"key":"x","last_write_index":5,"prefer_follower":true}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Follower behind redirects to leader

Follower unlikely to have index 999. Should redirect to leader.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ryw_read","msg_id":2,"key":"x","last_write_index":999,"prefer_follower":true}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Session Guarantees for Weakly Consistent Data](https://www.cs.utexas.edu/~lorenzo/corsi/cs380d/papers/SessionGuarantees.pdf): Formal definition of read-your-writes and other session guarantees

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
