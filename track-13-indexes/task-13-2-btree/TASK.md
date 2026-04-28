# Build B-Tree Index

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-2-btree>

Track: 13. Indexes
Task order: 2
Short title: B-Tree Index
Difficulty: intermediate

## Problem

Implement a B-Tree index supporting both point and range queries:

1. Internal nodes contain keys and child pointers
2. Leaf nodes contain keys and data pointers
3. Insert splits full nodes
4. All leaves at same depth (balanced)

B-Trees minimize disk I/O with high fanout - each read returns many keys.

## Concept Notes

### B-Trees

B-Trees are optimized for storage systems. Each node contains many keys (high fanout), reducing tree height. A tree with millions of keys might be only 3-4 levels deep, requiring 3-4 disk reads for any lookup.

### B-Tree vs B+Tree

In a B+Tree (most common in databases), all data lives in leaves, and leaves are linked for efficient range scans. Internal nodes contain only keys for routing.

## Concepts

- B-tree
- balanced tree
- range queries

## Hints

- Nodes contain multiple keys
- Keep tree balanced for O(log n)
- Handle node splits on insert

## Test Cases

### 1. B-Tree insert and search

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_insert","msg_id":2,"key":"foo","value":100}}
{"src":"c2","dest":"n1","body":{"type":"btree_search","msg_id":3,"key":"foo"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"btree_insert_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"btree_search_ok","in_reply_to":3,"msg_id":2,"found":true,"value":100}}
```

## Resources

- [B-Tree Visualization](https://www.cs.usfca.edu/~galles/visualization/BTree.html): Interactive B-tree visualization

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
