# Implement B-Tree Insert with Node Splits

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-2-btree-insert>

Track: 19. The Logger
Task order: 12
Short title: B-Tree Insert
Difficulty: advanced
Subtrack: B-Tree on Disk

## Problem

B-Tree insertion maintains the tree's balance invariant: all leaf nodes are always at the same depth. The key mechanism is the **node split** — when a node overflows, it splits into two nodes and promotes the middle key to the parent.

Insert algorithm:
1. **Find** the correct leaf node (binary search from root, same as lookup)
2. **Insert** the key in sorted position within the leaf
3. **Split if full**: if the leaf exceeds the maximum number of keys:
   a. Split the node into two halves
   b. The middle key is promoted to the parent
   c. The parent now has a new child and a new key — it may also need to split
4. **Root split**: if the root itself overflows, create a new root with the middle key and two children. The tree height increases by 1.

This recursive splitting ensures that the tree remains perfectly balanced — every path from root to leaf has the same length.

```json
Request:  {"type": "btree_insert", "msg_id": 1, "key": "user:50", "value": "Charlie"}
Response: {"type": "btree_insert_ok", "in_reply_to": 1, "splits": 0, "new_depth": 3}

Request:  {"type": "btree_insert", "msg_id": 2, "key": "user:75", "value": "Dave"}
Response: {"type": "btree_insert_ok", "in_reply_to": 2, "splits": 1, "split_keys": ["user:60"], "new_depth": 3}
```

## Concepts

- insert
- node split
- root split
- balancing
- overflow handling

## Hints

- To insert, first find the correct leaf node (same as search)
- If the leaf has room, insert the key in sorted order
- If the leaf is full, SPLIT it: create two nodes, push the middle key up to the parent
- The parent may also overflow and split, recursively up to the root
- Root split: the root splits into two children, a new root is created with the middle key -> tree grows by 1 level

## Test Cases

### 1. Insert into non-full leaf

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_insert","msg_id":2,"key":"k1","value":"v1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "btree_insert_ok", "in_reply_to": 2, "splits": 0, "msg_id": 1}}
```

### 2. Inserted key is retrievable

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_insert","msg_id":2,"key":"test","value":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":3,"key":"test"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "btree_insert_ok", "in_reply_to": 2, "splits": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "btree_search_ok", "in_reply_to": 3, "found": true, "value": "hello", "msg_id": 2}}
```

## Resources

- [B-Tree Insertion Algorithm](https://en.wikipedia.org/wiki/B-tree#Insertion): Detailed explanation of B-Tree insertion with node splitting algorithm

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
