# Implement a B-Tree Node and Search

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-1-btree-node>

Track: 19. The Logger
Task order: 11
Short title: B-Tree Node
Difficulty: intermediate
Subtrack: B-Tree on Disk

## Problem

The B-Tree is the most widely used on-disk data structure. PostgreSQL, MySQL InnoDB, SQLite, and virtually every relational database uses B-Trees for their indexes.

A B-Tree node maps to a fixed-size **page** on disk (typically 4KB, matching the OS page size). Each node holds:
- **Internal nodes**: sorted keys + child pointers. Each key acts as a separator between two subtrees.
- **Leaf nodes**: sorted keys + values (or pointers to data rows).

The search algorithm:
1. Start at the root node (1 disk read)
2. Binary search within the node to find the correct child pointer
3. Follow the pointer to the next node (1 disk read)
4. Repeat until reaching a leaf node
5. Binary search within the leaf for the key

With a branching factor of 500 (typical for 4KB pages), a 3-level B-Tree can store ~125 million keys, requiring only **3 disk reads** per lookup.

```json
Request:  {"type": "btree_search", "msg_id": 1, "key": "user:42"}
Response: {"type": "btree_search_ok", "in_reply_to": 1, "found": true, "value": "Alice", "disk_reads": 3, "depth": 3}

Request:  {"type": "btree_search", "msg_id": 2, "key": "user:999999"}
Response: {"type": "btree_search_ok", "in_reply_to": 2, "found": false, "disk_reads": 3, "depth": 3}

Request:  {"type": "btree_info", "msg_id": 3}
Response: {"type": "btree_info_ok", "in_reply_to": 3, "depth": 3, "total_nodes": 512, "page_size_bytes": 4096, "branching_factor": 500}
```

## Concepts

- B-Tree
- page
- node structure
- disk reads
- binary search

## Hints

- Each B-Tree node maps to a fixed-size disk page (typically 4KB)
- Internal nodes hold keys and child pointers; leaf nodes hold keys and values
- Search: binary search within a node to find the correct child pointer, then follow it to the next level
- A B-Tree of depth 3 with 4KB pages can hold millions of keys with only 3 disk reads per lookup
- The branching factor (keys per node) determines tree depth: higher branching = shallower tree

## Test Cases

### 1. Search finds existing key

btree_search_ok should show found: true with a value and disk_reads equal to tree depth.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":2,"key":"user:42"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Search for missing key returns not found

btree_search_ok should show found: false. disk_reads should still equal tree depth (full traversal).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":2,"key":"nonexistent"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [B-Tree Visualization](https://www.cs.usfca.edu/~galles/visualization/BTree.html): Interactive visualization tool for understanding B-Tree structure and operations

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
