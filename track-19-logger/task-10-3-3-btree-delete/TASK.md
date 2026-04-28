# Implement B-Tree Delete with Merge and Borrow

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-3-btree-delete>

Track: 19. The Logger
Task order: 13
Short title: B-Tree Delete
Difficulty: advanced
Subtrack: B-Tree on Disk

## Problem

B-Tree deletion is the most complex operation because it must maintain two invariants:
1. **Minimum occupancy**: every non-root node must have at least `ceil(order/2) - 1` keys
2. **Balance**: all leaf nodes remain at the same depth

Delete algorithm:
1. **Find** the key in the tree
2. **Delete from leaf**: remove the key. If the node still has enough keys, done.
3. **Handle underflow** (node has too few keys):
   a. **Borrow from sibling**: if a sibling has more than the minimum keys, rotate through the parent. The sibling gives a key to the parent, and the parent gives its separator key to the deficient node.
   b. **Merge with sibling**: if no sibling can lend, merge the node with a sibling and pull down the parent's separator key. This may cause the parent to underflow (recursion).
4. **Root collapse**: if the root has zero keys (because its only two children merged), the merged child becomes the new root.

```json
Request:  {"type": "btree_delete", "msg_id": 1, "key": "user:50"}
Response: {"type": "btree_delete_ok", "in_reply_to": 1, "deleted": true, "rebalance": "none"}

Request:  {"type": "btree_delete", "msg_id": 2, "key": "user:25"}
Response: {"type": "btree_delete_ok", "in_reply_to": 2, "deleted": true, "rebalance": "borrow_from_sibling"}

Request:  {"type": "btree_delete", "msg_id": 3, "key": "user:10"}
Response: {"type": "btree_delete_ok", "in_reply_to": 3, "deleted": true, "rebalance": "merge_with_sibling", "new_depth": 2}
```

## Concepts

- delete
- underflow
- merge
- borrow
- rebalancing
- minimum occupancy

## Hints

- B-Tree nodes must maintain a minimum number of keys (typically ceil(order/2) - 1)
- Deletion from a leaf: simply remove the key. If underflow occurs, rebalance.
- Borrow (rotation): steal a key from a sibling through the parent. Preferred over merging.
- Merge: if neither sibling can lend a key, merge the node with a sibling and pull down the parent separator key.
- If the root becomes empty after a merge, the merged child becomes the new root (tree shrinks by 1 level).

## Test Cases

### 1. Delete existing key successfully

btree_delete_ok should show deleted: true. Subsequent search should show found: false.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_insert","msg_id":2,"key":"k1","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"btree_delete","msg_id":3,"key":"k1"}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":4,"key":"k1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Delete non-existent key returns not found

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_delete","msg_id":2,"key":"nonexistent"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "btree_delete_ok", "in_reply_to": 2, "deleted": false, "msg_id": 1}}
```

## Resources

- [B-Tree Deletion Algorithm](https://en.wikipedia.org/wiki/B-tree#Deletion): B-Tree deletion with merge, borrow, and root collapse operations explained

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
