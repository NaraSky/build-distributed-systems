# Prove ZAB Sequential Consistency

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-3-sequential-consistency>

Track: 22. The Watcher
Task order: 13
Short title: Sequential Consistency
Difficulty: advanced
Subtrack: Consistency and the ZAB Protocol

## Problem

ZAB provides sequential consistency: all clients observe updates in the same total order. This is the fundamental consistency guarantee of ZooKeeper.

**Sequential consistency means**:
1. All updates from a single client are applied in the order they were sent (FIFO client order)
2. All clients see updates in the same total order (global ordering)
3. Reads may be slightly stale (a follower may not have the latest committed update yet)

**Test for sequential consistency**:
- Client A writes: `/x = 1`, then `/y = 2`
- Client B writes: `/x = 3`, then `/y = 4`
- All observers must see either {A before B} or {B before A}, never interleaved out of order
- Under eventual consistency, an observer might see `/x=3, /y=2` (inconsistent mix)

```json
Request:  {"type": "consistency_test", "msg_id": 1, "writes": [{"client": "A", "ops": [{"path": "/x", "value": "1"}, {"path": "/y", "value": "2"}]}, {"client": "B", "ops": [{"path": "/x", "value": "3"}, {"path": "/y", "value": "4"}]}]}
Response: {"type": "consistency_test_ok", "in_reply_to": 1, "total_order": ["A:/x=1", "A:/y=2", "B:/x=3", "B:/y=4"], "sequential_consistent": true, "violations": 0}
```

## Concepts

- sequential consistency
- total order
- linearizability vs sequential
- ordering test
- consistency verification

## Hints

- Sequential consistency: all clients see updates in the same order
- This is weaker than linearizability: reads may be stale (from a follower)
- Test: two clients write concurrently. All observers must see writes in the same order.
- This test would FAIL under eventual consistency but PASSES under ZAB
- ZAB guarantees FIFO client order + total order of all committed writes

## Test Cases

### 1. Sequential consistency test passes

consistency_test_ok should show sequential_consistent: true and violations: 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"consistency_test","msg_id":2,"writes":[{"client":"A","ops":[{"path":"/x","value":"1"}]},{"client":"B","ops":[{"path":"/y","value":"2"}]}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Client FIFO order preserved

In total_order, A:/a=1 must appear before A:/a=2 (FIFO per client).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"consistency_test","msg_id":2,"writes":[{"client":"A","ops":[{"path":"/a","value":"1"},{"path":"/a","value":"2"}]}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Consistency Guarantees](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkGuarantees): ZooKeeper documentation on sequential consistency and ordering guarantees

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
