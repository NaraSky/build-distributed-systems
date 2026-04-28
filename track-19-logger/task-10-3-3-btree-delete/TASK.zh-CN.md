# 实现 B-Tree Delete，包含Merge和Borrow

英文标题：Implement B-Tree Delete，包含Merge和Borrow
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-3-btree-delete>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：13
短标题：B-Tree Delete
难度：advanced
子主题：B-Tree on Disk

## 中文导读

本题要求你完成 `实现 B-Tree Delete，包含Merge和Borrow`。

重点关注：`delete`、`underflow`、`merge`、`borrow`、`rebalancing`。

建议先按提示逐步实现：B-Tree 节点 must maintain a minimum number of keys (typically ceil(order/2) - 1)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

B-Tree deletion is the most complex operation because it must maintain two invariants:
1. **Minimum occupancy**: every non-root 节点 must have at least `ceil(order/2) - 1` keys
2. **Balance**: all leaf 节点 remain at the same depth

Delete algorithm:
1. **Find** the key in the tree
2. **Delete from leaf**: remove the key. If the 节点 still has enough keys, done.
3. **Handle underflow** (节点 has too few keys):
   a. **Borrow from sibling**: if a sibling has more than the minimum keys, rotate through the parent. The sibling gives a key to the parent,和the parent gives its separator key to the deficient 节点.
   b. **Merge，包含sibling**: if no sibling can lend, merge the 节点，包含a sibling和pull down the parent's separator key. This may cause the parent to underflow (recursion).
4. **Root collapse**: if the root has zero keys (because its only two children merged), the merged child becomes the new root.

```JSON
请求:  {"type": "btree_delete", "msg_id": 1, "key": "user:50"}
响应: {"type": "btree_delete_ok", "in_reply_to": 1, "deleted": true, "rebalance": "none"}

请求:  {"type": "btree_delete", "msg_id": 2, "key": "user:25"}
响应: {"type": "btree_delete_ok", "in_reply_to": 2, "deleted": true, "rebalance": "borrow_from_sibling"}

请求:  {"type": "btree_delete", "msg_id": 3, "key": "user:10"}
响应: {"type": "btree_delete_ok", "in_reply_to": 3, "deleted": true, "rebalance": "merge_with_sibling", "new_depth": 2}
```

## 涉及概念

- `delete`
- `underflow`
- `merge`
- `borrow`
- `rebalancing`
- `minimum occupancy`

## 实现提示

- B-Tree 节点 must maintain a minimum number of keys (typically ceil(order/2) - 1)
- Deletion from a leaf: simply remove the key. If underflow occurs, rebalance.
- Borrow (rotation): steal a key from a sibling through the parent. Preferred over merging.
- Merge: if neither sibling can lend a key, merge the 节点，包含a sibling和pull down the parent separator key.
- If the root becomes empty after a merge, the merged child becomes the new root (tree shrinks by 1 level).

## 测试用例

### 1. Delete existing key successfully

btree_delete_ok should show deleted: true. Subsequent search should show found: false.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_insert","msg_id":2,"key":"k1","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"btree_delete","msg_id":3,"key":"k1"}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":4,"key":"k1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Delete non-existent key returns not found

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_delete","msg_id":2,"key":"nonexistent"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "btree_delete_ok", "in_reply_to": 2, "deleted": false, "msg_id": 1}}
```

## 参考资料

- [B-Tree Deletion Algorithm](https://en.wikipedia.org/wiki/B-tree#Deletion)：B-Tree deletion，包含merge, borrow,和root collapse operations explained

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
