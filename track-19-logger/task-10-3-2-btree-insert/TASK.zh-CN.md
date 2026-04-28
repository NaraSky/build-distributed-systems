# 实现 B-Tree Insert，包含Node Splits

英文标题：Implement B-Tree Insert，包含Node Splits
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-2-btree-insert>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：12
短标题：B-Tree Insert
难度：advanced
子主题：B-Tree on Disk

## 中文导读

本题要求你完成 `实现 B-Tree Insert，包含Node Splits`。

重点关注：`insert`、`node split`、`root split`、`balancing`、`overflow handling`。

建议先按提示逐步实现：To insert, first find the correct leaf 节点 (same as search)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

B-Tree insertion maintains the tree's balance invariant: all leaf 节点 are always at the same depth. The key mechanism is the **节点 split** — when a 节点 overflows, it splits into two 节点和promotes the middle key to the parent.

Insert algorithm:
1. **Find** the correct leaf 节点 (binary search from root, same as lookup)
2. **Insert** the key in sorted position within the leaf
3. **Split if full**: if the leaf exceeds the maximum number of keys:
   a. Split the 节点 into two halves
   b. The middle key is promoted to the parent
   c. The parent now has a new child和a new key — it may also need to split
4. **Root split**: if the root itself overflows, create a new root，包含the middle key和two children. The tree height increases by 1.

This recursive splitting ensures that the tree remains perfectly balanced — every path from root to leaf has the same length.

```JSON
请求:  {"type": "btree_insert", "msg_id": 1, "key": "user:50", "value": "Charlie"}
响应: {"type": "btree_insert_ok", "in_reply_to": 1, "splits": 0, "new_depth": 3}

请求:  {"type": "btree_insert", "msg_id": 2, "key": "user:75", "value": "Dave"}
响应: {"type": "btree_insert_ok", "in_reply_to": 2, "splits": 1, "split_keys": ["user:60"], "new_depth": 3}
```

## 涉及概念

- `insert`
- `node split`
- `root split`
- `balancing`
- `overflow handling`

## 实现提示

- To insert, first find the correct leaf 节点 (same as search)
- If the leaf has room, insert the key in sorted order
- If the leaf is full, SPLIT it: create two 节点, push the middle key up to the parent
- The parent may also overflow和split, recursively up to the root
- Root split: the root splits into two children, a new root is created，包含the middle key -> tree grows by 1 level

## 测试用例

### 1. Insert into non-full leaf

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_insert","msg_id":2,"key":"k1","value":"v1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "btree_insert_ok", "in_reply_to": 2, "splits": 0, "msg_id": 1}}
```

### 2. Inserted key is retrievable

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_insert","msg_id":2,"key":"test","value":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":3,"key":"test"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "btree_insert_ok", "in_reply_to": 2, "splits": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "btree_search_ok", "in_reply_to": 3, "found": true, "value": "hello", "msg_id": 2}}
```

## 参考资料

- [B-Tree Insertion Algorithm](https://en.wikipedia.org/wiki/B-tree#Insertion)：Detailed explanation of B-Tree insertion，包含节点 splitting algorithm

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
