# Implement Sequential Nodes for Ordering

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-5-sequential>

Track: 22. The Watcher
Task order: 5
Short title: Sequential Nodes
Difficulty: intermediate
Subtrack: The ZNode Data Model

## Problem

Sequential nodes have a unique, auto-incremented 10-digit suffix appended by ZooKeeper. They guarantee ordering even when multiple clients create concurrently.

**How it works**:
1. Client sends `Create("/election/candidate-", data, SEQUENTIAL)`
2. ZooKeeper appends a 10-digit monotonically increasing number
3. Result: `/election/candidate-0000000001`
4. Next create: `/election/candidate-0000000002`

**Use cases**:
- **Leader election**: each candidate creates a sequential ephemeral node. The lowest number is the leader.
- **Distributed queue**: producers create sequential nodes (enqueue), consumers process the lowest number (dequeue).
- **Barriers**: N processes create sequential nodes; when N nodes exist, the barrier is released.

```json
Request:  {"type": "znode_create", "msg_id": 1, "path": "/election/candidate-", "data": "n1", "ephemeral": true, "sequential": true, "session_id": "s1"}
Response: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/election/candidate-0000000001", "version": 0}

Request:  {"type": "znode_create", "msg_id": 2, "path": "/election/candidate-", "data": "n2", "ephemeral": true, "sequential": true, "session_id": "s2"}
Response: {"type": "znode_create_ok", "in_reply_to": 2, "path": "/election/candidate-0000000002", "version": 0}
```

## Concepts

- sequential node
- auto-incrementing
- distributed queue
- leader election
- ordering guarantee

## Hints

- Create("/election/candidate-", ..., SEQUENTIAL) produces /election/candidate-0000000001
- The 10-digit suffix is monotonically increasing (global counter per parent)
- Sequential nodes guarantee a unique, ordered name even with concurrent creates
- Use case: distributed queue — enqueue creates sequential, dequeue processes lowest
- Use case: leader election — lowest sequence number is the leader

## Test Cases

### 1. Sequential creates get increasing suffixes

Second path suffix should be greater than first.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/q/item-","data":"a","ephemeral":false,"sequential":true}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":3,"path":"/q/item-","data":"b","ephemeral":false,"sequential":true}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Sequential names are unique

Both created paths should be different (unique suffixes).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/s/n-","data":"","ephemeral":false,"sequential":true}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":3,"path":"/s/n-","data":"","ephemeral":false,"sequential":true}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Sequential Nodes](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#Sequence+Nodes+--+Unique+Naming): ZooKeeper documentation on sequential nodes and unique naming

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
