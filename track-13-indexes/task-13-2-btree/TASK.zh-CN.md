# 构建 B-Tree 索引

英文标题：Build B-Tree Index
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-2-btree>

课程：13. 索引
任务序号：2
短标题：B-Tree 索引
难度：intermediate

## 中文导读

本题要求你完成 `构建 B-Tree 索引`。

重点关注：`B-tree`、`balanced tree`、`range queries`。

建议先按提示逐步实现：节点 contain multiple keys。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a B-Tree 索引 supporting both point和range queries:

1. Internal 节点 contain keys和child pointers
2. Leaf 节点 contain keys和data pointers
3. Insert splits full 节点
4. All leaves at same depth (balanced)

B-Trees minimize disk I/O，包含high fanout - each read returns many keys.

## 概念说明

### B-Trees

B-Trees are optimized用于存储 systems. Each 节点 contains many keys (high fanout), reducing tree height. A tree，包含millions of keys might be only 3-4 levels deep, requiring 3-4 disk reads用于any lookup.

### B-Tree vs B+Tree

In a B+Tree (most common in databases), all data lives in leaves,和leaves are linked用于efficient range scans. Internal 节点 contain only keys用于routing.

## 涉及概念

- `B-tree`
- `balanced tree`
- `range queries`

## 实现提示

- 节点 contain multiple keys
- Keep tree balanced用于O(日志 n)
-处理节点 splits on insert

## 测试用例

### 1. B-Tree insert和search

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_insert","msg_id":2,"key":"foo","value":100}}
{"src":"c2","dest":"n1","body":{"type":"btree_search","msg_id":3,"key":"foo"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"btree_insert_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"btree_search_ok","in_reply_to":3,"msg_id":2,"found":true,"value":100}}
```

## 参考资料

- [B-Tree Visualization](https://www.cs.usfca.edu/~galles/visualization/BTree.html)：Interactive B-tree visualization

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
