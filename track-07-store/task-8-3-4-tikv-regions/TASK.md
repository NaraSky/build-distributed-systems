# Build a Mini TiKV with Raft + MVCC Regions

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-4-tikv-regions>

Track: 7. The Store
Task order: 14
Short title: TiKV Regions
Difficulty: advanced
Subtrack: Transactions on Raft

## Problem

Build a mini version of TiKV: partition the key space into regions, each with its own Raft group and MVCC storage.

```json
Request:  {"type": "region_put", "msg_id": 1, "key": "user:1", "value": "Alice"}
Response: {"type": "region_put_ok", "in_reply_to": 1, "region_id": 1, "key_range": ["a", "m"]}

Request:  {"type": "region_get", "msg_id": 2, "key": "user:1"}
Response: {"type": "region_get_ok", "in_reply_to": 2, "value": "Alice", "region_id": 1}

Request:  {"type": "region_info", "msg_id": 3}
Response: {"type": "region_info_ok", "in_reply_to": 3, "regions": [
    {"id": 1, "range": ["a", "m"], "leader": "n1", "size_bytes": 1024},
    {"id": 2, "range": ["m", "z"], "leader": "n2", "size_bytes": 512}
]}

Request:  {"type": "region_split", "msg_id": 4, "region_id": 1, "split_key": "g"}
Response: {"type": "region_split_ok", "in_reply_to": 4, "new_regions": [
    {"id": 1, "range": ["a", "g"]},
    {"id": 3, "range": ["g", "m"]}
]}
```

## Concepts

- TiKV
- regions
- range partitioning
- Raft per region
- multi-region

## Hints

- TiKV splits the key space into ranges called regions
- Each region has its own Raft group for replication
- A region splits when it gets too large (e.g., > 96MB)
- Cross-region transactions use 2-phase commit
- The placement driver (PD) manages region-to-node mapping

## Test Cases

### 1. Put routes to correct region

region_put_ok should include the region_id routing to the correct range.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"region_put","msg_id":2,"key":"apple","value":"fruit"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Region info shows partitions

region_info_ok should list at least 1 region with id, range, and leader.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"region_info","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [TiKV Architecture](https://tikv.org/docs/deep-dive/introduction/): TiKV deep dive: regions, Raft groups, and MVCC

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
