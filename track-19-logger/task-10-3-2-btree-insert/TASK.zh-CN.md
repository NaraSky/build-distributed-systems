# 实现 B 树插入与节点分裂

网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-2-btree-insert>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：12
短标题：B 树插入
难度：高级
子主题：磁盘上的 B 树

## 中文导读

上一题你实现了 B 树的查找功能，这道题让你实现插入操作。插入的难点在于：当一个节点装满了怎么办？答案是"分裂"——把满了的节点一分为二，把中间的键提升到父节点。如果父节点也满了，就继续往上分裂，直到根节点。这种递归分裂机制保证了 B 树永远保持平衡。

理解节点分裂是掌握 B 树的关键，也是理解数据库索引维护开销的基础。

## 题目说明

B 树的插入操作需要始终维护一个核心不变量：所有叶子节点必须在同一深度。实现这一点的关键机制是**节点分裂（Node Split）**——当一个节点装不下更多的键时，它会一分为二，并把中间的键提升给父节点。

插入算法的具体步骤：

1. **查找**：从根节点开始，用二分查找定位到正确的叶子节点（这个过程和查找操作完全一样）
2. **插入**：把新键按排序位置插入叶子节点
3. **溢出则分裂**：如果叶子节点的键数量超过了上限：
   a. 把节点分成左右两半
   b. 把中间的键提升到父节点
   c. 父节点因此多了一个键和一个子节点——它也可能因此溢出并需要分裂
4. **根节点分裂**：如果根节点本身也溢出了，就创建一个新的根节点，用中间键作为分隔，原来的两半作为左右子节点。此时树的高度增加 1 层。

这种递归的分裂机制确保了 B 树始终保持完美平衡——从根到任意叶子的路径长度都相同。你可以把它想象成一个书架：每格放满了就拆成两格，如果整个书架都满了，就再加一层。

```json
Request:  {"type": "btree_insert", "msg_id": 1, "key": "user:50", "value": "Charlie"}
Response: {"type": "btree_insert_ok", "in_reply_to": 1, "splits": 0, "new_depth": 3}

Request:  {"type": "btree_insert", "msg_id": 2, "key": "user:75", "value": "Dave"}
Response: {"type": "btree_insert_ok", "in_reply_to": 2, "splits": 1, "split_keys": ["user:60"], "new_depth": 3}
```

## 涉及概念

- `insert`
- `node split`
- `root split`
- `balancing`
- `overflow handling`

## 实现提示

- 插入时，先用查找的方式定位到正确的叶子节点
- 如果叶子节点还有空间，直接按排序位置插入新键即可
- 如果叶子节点已满，执行分裂：创建两个节点，将中间键向上推给父节点
- 父节点也可能因此满溢并需要分裂，这个过程会一路递归向上直到根节点
- 根节点分裂时：根节点一分为二成为两个子节点，创建新的根节点持有中间键，树的高度增加 1 层

## 测试用例

### 1. 向未满的叶子节点插入

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

### 2. 插入后能成功查找到该键

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

- [B-Tree Insertion Algorithm](https://en.wikipedia.org/wiki/B-tree#Insertion)：维基百科上对 B 树插入算法和节点分裂机制的详细讲解

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
