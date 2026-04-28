# 实现 B 树节点与查找

网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-1-btree-node>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：11
短标题：B 树节点
难度：进阶
子主题：磁盘上的 B 树

## 中文导读

你在数据库中执行一条查询，哪怕表里有上亿条数据，结果也几乎瞬间返回。背后的秘密就是 B 树（B-Tree）。PostgreSQL、MySQL、SQLite 等几乎所有关系型数据库都用 B 树来构建索引。

这道题让你实现 B 树最基础的部分：节点的数据结构和查找操作。你将理解 B 树是如何把数据组织在固定大小的磁盘页上，以及为什么只需要寥寥几次磁盘读取就能在上亿条记录中找到目标。

## 题目说明

B 树是使用最广泛的磁盘数据结构。PostgreSQL、MySQL InnoDB、SQLite，以及几乎所有的关系型数据库，都用 B 树来实现索引。

B 树的每个节点对应磁盘上一个固定大小的**页（Page）**，通常为 4KB，刚好和操作系统的内存页大小一致。节点分为两种类型：

- **内部节点**：存放有序的键和子节点指针。你可以把每个键想象成一个"路标"，告诉你接下来该往左走还是往右走。
- **叶子节点**：存放有序的键和对应的值（或者指向实际数据行的指针），这里才是数据真正存放的地方。

查找算法的流程如下：
1. 从根节点开始，读取根节点所在的页（1 次磁盘读取）
2. 在当前节点内用二分查找（Binary Search）定位到正确的子节点指针
3. 沿着指针跳转到下一层节点（1 次磁盘读取）
4. 重复上述过程，直到到达叶子节点
5. 在叶子节点内用二分查找定位目标键

当分支因子（Branching Factor）为 500（4KB 页的典型值）时，一棵仅 3 层深的 B 树就可以存储约 1.25 亿个键，每次查找只需要 **3 次磁盘读取**。这就是 B 树高效的秘密：树非常"矮胖"，层数极少。

```json
Request:  {"type": "btree_search", "msg_id": 1, "key": "user:42"}
Response: {"type": "btree_search_ok", "in_reply_to": 1, "found": true, "value": "Alice", "disk_reads": 3, "depth": 3}

Request:  {"type": "btree_search", "msg_id": 2, "key": "user:999999"}
Response: {"type": "btree_search_ok", "in_reply_to": 2, "found": false, "disk_reads": 3, "depth": 3}

Request:  {"type": "btree_info", "msg_id": 3}
Response: {"type": "btree_info_ok", "in_reply_to": 3, "depth": 3, "total_nodes": 512, "page_size_bytes": 4096, "branching_factor": 500}
```

## 涉及概念

- `B-Tree`
- `page`
- `node structure`
- `disk reads`
- `binary search`

## 实现提示

- 每个 B 树节点对应磁盘上一个固定大小的页（通常 4KB）
- 内部节点存放键和子节点指针；叶子节点存放键和值
- 查找时在节点内部用二分查找定位正确的子节点指针，然后跳转到下一层
- 深度为 3、页大小为 4KB 的 B 树可以容纳数百万个键，每次查找只需 3 次磁盘读取
- 分支因子（每个节点能存放的键数量）决定了树的深度：分支因子越大，树越矮，查找越快

## 测试用例

### 1. 查找已存在的键

返回的 `btree_search_ok` 应包含 `found: true`、对应的值，以及等于树深度的 `disk_reads`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_search","msg_id":2,"key":"user:42"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 查找不存在的键应返回未找到

返回的 `btree_search_ok` 应包含 `found: false`。`disk_reads` 仍然等于树的深度，因为需要从根到叶子完整遍历一条路径才能确定键不存在。

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

- [B-Tree Visualization](https://www.cs.usfca.edu/~galles/visualization/BTree.html)：交互式的 B 树可视化工具，可以直观地观察 B 树的结构和各种操作过程

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
