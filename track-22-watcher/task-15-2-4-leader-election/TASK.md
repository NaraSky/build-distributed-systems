# Build Leader Election with ZooKeeper

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-4-leader-election>

Track: 22. The Watcher
Task order: 9
Short title: Leader Election
Difficulty: advanced
Subtrack: Watches and Sessions

## Problem

Leader election in ZooKeeper uses ephemeral sequential nodes. Each candidate creates a node, and the one with the lowest sequence number is the leader.

**Election algorithm**:
1. Each candidate creates: `/election/candidate-` (EPHEMERAL + SEQUENTIAL)
2. Get all children of `/election` and sort by sequence number
3. If your node has the lowest number, you are the **leader**
4. Otherwise, watch the node immediately before yours
5. If the leader crashes, its ephemeral node is deleted
6. The next candidate's watch fires, and it checks if it is now the lowest

**Automatic re-election**: because nodes are ephemeral, leader failure triggers automatic deletion, which triggers the next candidate's watch, causing seamless failover.

```json
Request:  {"type": "election_join", "msg_id": 1, "path": "/election", "candidate": "n1", "session_id": "s1"}
Response: {"type": "election_join_ok", "in_reply_to": 1, "node": "/election/candidate-0000000001", "is_leader": true, "leader": "n1"}

Request:  {"type": "election_status", "msg_id": 2, "path": "/election"}
Response: {"type": "election_status_ok", "in_reply_to": 2, "leader": "n1", "candidates": ["n1", "n2", "n3"], "ordered_nodes": ["/election/candidate-0000000001", "/election/candidate-0000000002", "/election/candidate-0000000003"]}
```

## Concepts

- leader election
- ephemeral sequential
- smallest number wins
- watch predecessor
- automatic re-election

## Hints

- Each candidate creates an ephemeral sequential node under /election
- The node with the lowest sequence number is the leader
- Other candidates watch the node immediately before them
- If the leader crashes, its ephemeral node is deleted, triggering re-election
- The next-lowest numbered node automatically becomes the new leader

## Test Cases

### 1. First candidate becomes leader

election_join_ok should show is_leader: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"election_join","msg_id":2,"path":"/election","candidate":"n1","session_id":"s1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Second candidate is follower

Second join should show is_leader: false and leader: "n1".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"election_join","msg_id":2,"path":"/election","candidate":"n1","session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"election_join","msg_id":3,"path":"/election","candidate":"n2","session_id":"s2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Leader Election](https://zookeeper.apache.org/doc/current/recipes.html#sc_leaderElection): ZooKeeper documentation on the leader election recipe

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
