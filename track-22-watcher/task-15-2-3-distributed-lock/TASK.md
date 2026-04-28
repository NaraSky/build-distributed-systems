# Build a Distributed Lock with ZooKeeper Primitives

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-3-distributed-lock>

Track: 22. The Watcher
Task order: 8
Short title: Distributed Lock
Difficulty: advanced
Subtrack: Watches and Sessions

## Problem

Building a distributed lock with ZooKeeper uses ephemeral sequential nodes to create a fair, deadlock-free locking mechanism.

**Lock algorithm** (avoids "herd effect"):
1. Create an ephemeral sequential node: `/locks/lock-` -> `/locks/lock-0000000005`
2. Get all children of `/locks` and sort by sequence number
3. If your node has the **lowest** sequence number, you hold the lock. Done.
4. Otherwise, watch the node **immediately before** yours in sorted order
5. When that node is deleted (predecessor released the lock), re-check step 3
6. Release: simply delete your node (or let the ephemeral timeout handle it on crash)

**Why watch only the predecessor?** If all waiters watched the lock holder, a single release would trigger N watch events (herd effect). Watching only the predecessor means only ONE client is notified.

```json
Request:  {"type": "lock_acquire", "msg_id": 1, "lock_path": "/locks/my-lock", "session_id": "s1"}
Response: {"type": "lock_acquire_ok", "in_reply_to": 1, "lock_node": "/locks/my-lock/lock-0000000001", "acquired": true, "position": 1}

Request:  {"type": "lock_release", "msg_id": 2, "lock_node": "/locks/my-lock/lock-0000000001"}
Response: {"type": "lock_release_ok", "in_reply_to": 2, "released": true}
```

## Concepts

- distributed lock
- ephemeral sequential
- herd effect
- watch predecessor
- fair locking

## Hints

- Create an ephemeral sequential node under /locks: /locks/lock-0000000001
- Get all children of /locks and sort them by sequence number
- If your node has the lowest number, you hold the lock
- Otherwise, watch the node immediately BEFORE yours (avoids herd effect)
- When that node is deleted (lock released), re-check if you are now the lowest

## Test Cases

### 1. Acquire lock when no contention

lock_acquire_ok should show acquired: true and position: 1.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_acquire","msg_id":2,"lock_path":"/locks/l1","session_id":"s1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Second acquirer waits in queue

First should show acquired: true, second should show acquired: false with position: 2.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_acquire","msg_id":2,"lock_path":"/locks/l2","session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"lock_acquire","msg_id":3,"lock_path":"/locks/l2","session_id":"s2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Lock Recipe](https://zookeeper.apache.org/doc/current/recipes.html#sc_recipes_Locks): ZooKeeper documentation on the distributed lock recipe

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
