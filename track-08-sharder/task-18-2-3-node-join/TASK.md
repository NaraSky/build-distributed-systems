# Handle Node Addition with Minimal Key Migration

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-3-node-join>

Track: 8. The Sharder
Task order: 8
Short title: Node Join
Difficulty: intermediate
Subtrack: Consistent Hashing

## Problem

When a node joins, it takes over a portion of the key space from its clockwise neighbor. Only the keys that now fall in the new node's range need to migrate.

**Join process**:
1. New node N4 calculates its position on the ring
2. N4 finds its clockwise neighbor (successor) N2
3. Keys between N4's counter-clockwise neighbor and N4 are transferred from N2 to N4
4. Only ~1/N of total keys are affected (minimal disruption)

**With virtual nodes**: the new node takes V positions on the ring, taking small ranges from multiple existing nodes. This distributes the migration load evenly.

```json
Request:  {"type": "ring_add_node", "msg_id": 1, "new_node": "n4"}
Response: {"type": "ring_add_node_ok", "in_reply_to": 1, "keys_migrated": 250, "total_keys": 1000, "migration_pct": 25.0, "source_nodes": ["n1", "n2", "n3"]}
```

## Concepts

- node addition
- key migration
- minimal disruption
- predecessor takeover
- data transfer

## Hints

- When a new node joins, it takes keys from its clockwise neighbor
- Only keys between the new node and its counter-clockwise neighbor migrate
- This is ~1/N of total keys (vs. nearly 100% with modulo hashing)
- During migration, the old owner continues serving reads for migrating keys
- After migration completes, redirect new requests to the new owner

## Test Cases

### 1. Node join migrates roughly 1/N keys

migration_pct should be roughly 25% (1/4 for 4 nodes).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_add_node","msg_id":2,"new_node":"n4"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Keys are still accessible after migration

ring_lookup_ok should return the new owner for migrated keys.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_add_node","msg_id":2,"new_node":"n3"}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":3,"key":"migrated-key"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Consistent Hashing: Node Addition](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf): Karger et al. - Consistent Hashing and Random Trees

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
