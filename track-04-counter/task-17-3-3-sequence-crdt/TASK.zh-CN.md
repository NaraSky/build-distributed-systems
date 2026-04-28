# 实现序列 CRDT 以支持协同文本编辑

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-3-sequence-crdt>

课程：4. 计数器：分布式状态与 CRDT
任务序号：13
短标题：Sequence CRDT
难度：高级
子主题：更多 CRDT

## 中文导读

这道题让你实现序列 CRDT，支持多人同时编辑同一篇文档而不产生冲突。它使用 RGA（可复制增长数组）算法，为每个字符分配一个全局唯一且有序的位置标识符。这是 Google Docs 等协同编辑工具背后的核心技术思想。

## 题目说明

序列 CRDT（Sequence CRDT）支持协同文本编辑，允许多个用户同时输入而不产生冲突。RGA（Replicated Growable Array，可复制增长数组）为每个字符分配一个唯一且有序的位置标识符。

**RGA 设计**：
- 每个字符拥有一个唯一 ID：`(Lamport 时间戳, 节点 ID)`
- 字符按 ID 排序，文档就是排序后的字符序列
- 在位置 P1 和 P2 之间插入：创建一个介于它们之间的新 ID
- 删除：将字符标记为墓碑（Tombstone），保留 ID 用于排序

**并发插入**：如果两个用户在同一位置插入字符，用节点 ID 来决定先后顺序。这确保了所有副本上的字符顺序是确定一致的。

```json
Request:  {"type": "seq_insert", "msg_id": 1, "position": 0, "char": "H"}
Response: {"type": "seq_insert_ok", "in_reply_to": 1, "id": "1-n1"}

Request:  {"type": "seq_read", "msg_id": 2}
Response: {"type": "seq_read_ok", "in_reply_to": 2, "text": "Hello", "length": 5}
```

## 涉及概念

- `sequence CRDT`
- `RGA`
- `collaborative editing`
- `position identifiers`
- `concurrent inserts`

## 实现提示

- 使用 RGA（可复制增长数组）：每个字符都有一个唯一的位置 ID
- 位置 ID 是有序的且不会改变，新字符获取介于相邻字符之间的 ID
- 删除操作将字符标记为墓碑（永远不会物理删除）
- 在同一位置的并发插入按节点 ID 排序（作为平局裁决规则）
- 最终文档是按位置顺序排列的所有非墓碑字符的序列

## 测试用例

### 1. 插入并读取字符

验证 seq_read_ok 的 text 应为 "Hi"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":2,"position":0,"char":"H"}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":3,"position":1,"char":"i"}}
{"src":"c1","dest":"n1","body":{"type":"seq_read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 删除操作将字符标记为墓碑

验证 seq_read_ok 的 text 应为 "B"（A 已被删除）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":2,"position":0,"char":"A"}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":3,"position":1,"char":"B"}}
{"src":"c1","dest":"n1","body":{"type":"seq_delete","msg_id":4,"position":0}}
{"src":"c1","dest":"n1","body":{"type":"seq_read","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [RGA: Replicated Growable Array](https://doi.org/10.1016/j.jpdc.2010.12.006)：Roh 等人关于可复制抽象数据类型的论文，协同应用的构建基石

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
