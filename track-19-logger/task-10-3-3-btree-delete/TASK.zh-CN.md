# 实现 B 树删除：合并与借用

网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-3-btree-delete>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：13
短标题：B 树删除
难度：高级
子主题：磁盘上的 B 树

## 中文导读

插入操作担心的是节点"太满"，删除操作担心的则是节点"太空"。当删除一个键导致节点中的键数量低于最小要求时，就需要想办法从旁边的兄弟节点"借"一个键过来；如果兄弟也没有多余的键可借，就只能把两个节点合并成一个。

这道题是 B 树三部曲的最后一题，也是最复杂的一题。掌握了删除操作中的借用和合并机制，你对 B 树的理解就完整了。

## 题目说明

B 树的删除操作是最复杂的，因为它必须同时维护两个不变量：

1. **最小占用率**：每个非根节点必须至少有 `ceil(order/2) - 1` 个键。这个约束确保了 B 树不会退化成一棵又高又瘦的树。
2. **平衡性**：所有叶子节点必须保持在同一深度。

删除算法的具体步骤：

1. **查找**：在树中找到要删除的键
2. **从叶子节点删除**：直接移除该键。如果删除后节点中的键数量仍然满足最小要求，操作就完成了。
3. **处理下溢（Underflow）**——如果节点的键太少了：
   a. **从兄弟节点借用（Borrow）**：如果某个相邻的兄弟节点拥有超过最低要求的键，就通过父节点做一次"旋转"。具体来说，兄弟节点把一个键交给父节点，父节点把它原有的分隔键交给当前不够的节点。这就像两个人之间通过中间人交换物品。
   b. **与兄弟节点合并（Merge）**：如果左右兄弟都没有多余的键可以借出，就把当前节点和一个兄弟节点合并成一个，同时从父节点拉下分隔键。合并后父节点少了一个键和一个子节点，它自己也可能因此下溢，需要递归处理。
4. **根节点坍缩**：如果根节点在合并后变成了零个键（因为它仅有的两个子节点合并成了一个），那么这个合并后的子节点就成为新的根节点，树的高度减少 1 层。

```json
Request:  {"type": "btree_delete", "msg_id": 1, "key": "user:50"}
Response: {"type": "btree_delete_ok", "in_reply_to": 1, "deleted": true, "rebalance": "none"}

Request:  {"type": "btree_delete", "msg_id": 2, "key": "user:25"}
Response: {"type": "btree_delete_ok", "in_reply_to": 2, "deleted": true, "rebalance": "borrow_from_sibling"}

Request:  {"type": "btree_delete", "msg_id": 3, "key": "user:10"}
Response: {"type": "btree_delete_ok", "in_reply_to": 3, "deleted": true, "rebalance": "merge_with_sibling", "new_depth": 2}
```

## 涉及概念

- `delete`
- `underflow`
- `merge`
- `borrow`
- `rebalancing`
- `minimum occupancy`

## 实现提示

- B 树节点必须维持最少键数（通常为 ceil(order/2) - 1），低于这个数就叫"下溢"
- 从叶子节点删除很简单：直接移除键。但如果导致了下溢，就需要重新平衡
- 优先借用：从拥有多余键的兄弟节点通过父节点"旋转"一个键过来。借用比合并开销小
- 不得不合并时：把当前节点和兄弟节点合并为一个，并从父节点拉下分隔键
- 如果根节点在合并后变空了，合并后的子节点直接升格为新的根节点，树的高度减少 1 层

## 测试用例

### 1. 成功删除已存在的键

返回的 `btree_delete_ok` 应包含 `deleted: true`。后续查找该键应返回 `found: false`。

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

### 2. 删除不存在的键应返回未删除

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

- [B-Tree Deletion Algorithm](https://en.wikipedia.org/wiki/B-tree#Deletion)：维基百科上对 B 树删除操作的详细讲解，涵盖合并、借用和根节点坍缩

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
