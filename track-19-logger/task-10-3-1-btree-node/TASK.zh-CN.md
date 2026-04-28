# 实现 a B-Tree Node和Search

英文标题：Implement a B-Tree Node和Search
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-1-btree-node>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：11
短标题：B-Tree Node
难度：intermediate
子主题：B-Tree on Disk

## 中文导读

本题要求你完成 `实现 a B-Tree Node和Search`。

重点关注：`B-Tree`、`page`、`node structure`、`disk reads`、`binary search`。

建议先按提示逐步实现：Each B-Tree 节点 maps to a fixed-size disk page (typically 4KB)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The B-Tree is the most widely used on-disk data structure. PostgreSQL, MySQL InnoDB, SQLite,和virtually every relational database uses B-Trees用于their indexes.

A B-Tree 节点 maps to a fixed-size **page** on disk (typically 4KB, matching the OS page size). Each 节点 holds:
- **Internal 节点**: sorted keys + child pointers. Each key acts as a separator between two subtrees.
- **Leaf 节点**: sorted keys + values (or pointers to data rows).

The search algorithm:
1. Start at the root 节点 (1 disk read)
2. Binary search within the 节点 to find the correct child pointer
3. Follow the pointer to the next 节点 (1 disk read)
4. Repeat until reaching a leaf 节点
5. Binary search within the leaf用于the key

With a branching factor of 500 (typical用于4KB pages), a 3-level B-Tree can store ~125 million keys, requiring only **3 disk reads** per lookup.

```JSON
请求:  {"type": "btree_search", "msg_id": 1, "key": "user:42"}
响应: {"type": "btree_search_ok", "in_reply_to": 1, "found": true, "value": "Alice", "disk_reads": 3, "depth": 3}

请求:  {"type": "btree_search", "msg_id": 2, "key": "user:999999"}
响应: {"type": "btree_search_ok", "in_reply_to": 2, "found": false, "disk_reads": 3, "depth": 3}

请求:  {"type": "btree_info", "msg_id": 3}
响应: {"type": "btree_info_ok", "in_reply_to": 3, "depth": 3, "total_nodes": 512, "page_size_bytes": 4096, "branching_factor": 500}
```

## 涉及概念

- `B-Tree`
- `page`
- `node structure`
- `disk reads`
- `binary search`

## 实现提示

- Each B-Tree 节点 maps to a fixed-size disk page (typically 4KB)
- Internal 节点 hold keys和child pointers; leaf 节点 hold keys和values
- Search: binary search within a 节点 to find the correct child pointer, then follow it to the next level
- A B-Tree of depth 3，包含4KB pages can hold millions of keys，包含only 3 disk reads per lookup
- The branching factor (keys per 节点) determines tree depth: higher branching = shallower tree

## 测试用例

### 1. Search finds existing key

btree_search_ok should show found: true，包含a value和disk_reads equal to tree depth.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":2,"key":"user:42"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Search用于missing key returns not found

btree_search_ok should show found: false. disk_reads should still equal tree depth (full traversal).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":2,"key":"nonexistent"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [B-Tree Visualization](https://www.cs.usfca.edu/~galles/visualization/BTree.html)：Interactive visualization tool用于understanding B-Tree structure和operations

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
