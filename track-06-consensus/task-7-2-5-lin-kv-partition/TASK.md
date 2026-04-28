# Pass Linearizable KV with Network Partitions

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-5-lin-kv-partition>

Track: 6. The Consensus
Task order: 10
Short title: Lin-KV Partitions
Difficulty: advanced
Subtrack: Commitment and Application

## Problem

The ultimate test: pass a linearizable key-value workload with 5 nodes under network partitions. This combines everything: leader election, log replication, commitment, snapshots, and partition handling.

Your system must:
1. Continue serving reads and writes when a majority is available
2. Reject requests when only a minority partition is reachable
3. Recover correctly after partition heals
4. Maintain linearizability throughout

```json
Request:  {"type": "partition_test", "msg_id": 1, "cluster_size": 5, "operations": 100, "partition_after_op": 30, "heal_after_op": 70}
Response: {"type": "partition_test_ok", "in_reply_to": 1, "total_ops": 100, "ops_during_partition": 40, "ops_succeeded": 85, "ops_rejected": 15, "linearizable": true}

Request:  {"type": "verify_linearizability", "msg_id": 2, "history": [...]}
Response: {"type": "verify_linearizability_ok", "in_reply_to": 2, "linearizable": true, "violations": []}
```

## Concepts

- linearizability
- network partition
- Maelstrom
- end-to-end correctness

## Hints

- Network partitions split the cluster into minority and majority groups
- The minority partition must stop serving writes (no quorum)
- The majority partition elects a new leader and continues serving
- After partition heals, the minority nodes must sync up via log replication
- Linearizability means every read returns the most recent committed write

## Test Cases

### 1. Partition test maintains linearizability

partition_test_ok should show linearizable: true with some ops_rejected during minority partition.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4","n5"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_test","msg_id":2,"cluster_size":5,"operations":20,"partition_after_op":5,"heal_after_op":15}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Writes rejected in minority partition

ops_rejected should be > 0 since minority nodes cannot form a quorum.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4","n5"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_test","msg_id":2,"cluster_size":5,"operations":10,"partition_after_op":2,"heal_after_op":8}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Maelstrom - Linearizable KV Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-lin-kv): Maelstrom lin-kv workload specification for testing linearizability

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
