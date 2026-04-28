# 构建 B 树索引

英文标题：Build B-Tree Index
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-2-btree>

课程：13. 索引
任务序号：2
短标题：B 树索引
难度：进阶

## 中文导读

这道题要求你实现一个 B 树（B-Tree）索引，它既能支持精确查找，也能支持范围查询。B 树是几乎所有关系型数据库（如 MySQL、PostgreSQL）默认使用的索引结构。与哈希索引不同，B 树通过保持有序性来同时支持等值查询和范围查询，是数据库领域最重要的数据结构之一。

## 题目说明

实现一个支持精确查找和范围查询的 B 树索引：

1. 内部节点（Internal Node）包含键和子节点指针
2. 叶子节点（Leaf Node）包含键和数据指针
3. 插入时，如果节点已满则进行分裂
4. 所有叶子节点处于同一深度（保持平衡）

B 树通过高扇出（每个节点存储多个键）来最小化磁盘读取次数——每次磁盘读取都能获得许多键。

## 概念说明

### B 树

B 树是为存储系统优化的数据结构。每个节点包含多个键（高扇出），这使得树的高度很低。一棵包含数百万个键的 B 树可能只有 3 到 4 层深，这意味着任何一次查找只需要 3 到 4 次磁盘读取。你可以把 B 树想象成一棵非常"矮胖"的树——每个节点都有很多分支，所以不需要太多层就能覆盖大量数据。

### B 树与 B+ 树

在 B+ 树（数据库中最常用的变种）中，所有实际数据都存储在叶子节点中，而且叶子节点之间通过链表相连，方便高效地进行范围扫描。内部节点只包含用于路由的键。

## 涉及概念

- `B-tree`
- `balanced tree`
- `range queries`

## 实现提示

- 每个节点包含多个键
- 保持树的平衡以确保 O(log n) 的查找时间
- 插入时处理节点分裂

## 测试用例

### 1. B 树插入与查找

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

- [B-Tree Visualization](https://www.cs.usfca.edu/~galles/visualization/BTree.html)：交互式 B 树可视化工具

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
