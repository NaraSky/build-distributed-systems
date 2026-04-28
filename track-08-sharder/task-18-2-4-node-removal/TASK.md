# Handle Node Removal with Graceful and Crash Recovery

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-4-node-removal>

Track: 8. The Sharder
Task order: 9
Short title: Node Removal
Difficulty: advanced
Subtrack: Consistent Hashing

## Problem

When a node leaves the ring (graceful shutdown or crash), its key range must be taken over by its successor. The two scenarios require different handling.

**Graceful shutdown**:
1. Node announces it is leaving
2. Node transfers all its keys to its clockwise successor(s)
3. Ring topology is updated
4. No data loss, minimal disruption

**Crash recovery**:
1. Other nodes detect the failure (missed heartbeats)
2. The successor takes over the key range
3. Data is recovered from replica copies
4. New replicas are created to restore the replication factor

```json
Request:  {"type": "ring_remove_node", "msg_id": 1, "node": "n2", "mode": "graceful"}
Response: {"type": "ring_remove_node_ok", "in_reply_to": 1, "keys_migrated": 333, "target_nodes": ["n1", "n3"], "mode": "graceful"}
```

## Concepts

- node removal
- graceful shutdown
- crash recovery
- key takeover
- successor promotion

## Hints

- On graceful shutdown: node transfers its keys to its clockwise successor before leaving
- On crash: the successor detects the failure and takes over the key range
- Graceful is faster (pre-transfer), crash requires recovery from replicas
- With virtual nodes, keys from the removed vnodes distribute to multiple successors
- Replica copies ensure no data loss even on crash

## Test Cases

### 1. Graceful removal migrates keys

ring_remove_node_ok should show keys migrated to remaining nodes.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_remove_node","msg_id":2,"node":"n2","mode":"graceful"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Crash recovery takes over key range

Crash mode should trigger recovery from replicas.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_remove_node","msg_id":2,"node":"n3","mode":"crash"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Consistent Hashing: Node Removal](https://www.akamai.com/us/en/multimedia/documents/technical-publication/consistent-hashing-and-random-trees-distributed-caching-protocols-for-relieving-hot-spots-on-the-world-wide-web-technical-publication.pdf): Akamai consistent hashing paper on node join/leave strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
