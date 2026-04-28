# 实现观察-删除集合

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-1-or-set>

课程：4. 计数器：分布式状态与 CRDT
任务序号：11
短标题：OR-Set
难度：高级
子主题：更多 CRDT

## 中文导读

这道题要求你实现观察-删除集合（OR-Set），它解决了分布式集合中最棘手的问题：当两个节点同时对同一个元素执行添加和删除操作时，最终结果应该是什么？观察-删除集合的答案是"添加优先"，其核心设计是为每次添加操作生成一个唯一标签，删除时只移除已经观察到的标签。

## 题目说明

观察-删除集合（OR-Set，Observed-Remove Set）解决了分布式环境下"并发添加和删除同一个元素"的经典难题。它的核心思路是：每次添加元素时，都给这个元素附上一个全局唯一的标签；删除时，只删除当前已经看到的那些标签。

**朴素集合的问题**：假设节点（Node）A 添加了元素 "x"，与此同时节点 B 删除了 "x"，最终结果会怎样？如果使用简单的集合实现，结果完全取决于消息的到达顺序，这在分布式环境下是不可预测的。

**观察-删除集合的解决方案**：
- `add("x")`：存储 `("x", tag_1)`，其中 `tag_1` 是一个唯一的标识符
- `remove("x")`：找到当前可见的所有关于 "x" 的记录并全部删除，比如 `{("x", tag_1)}`
- 如果节点 A 执行 `add("x")` 的同时节点 B 执行 `remove("x")`：节点 A 的添加操作会产生一个新标签 `tag_2`，而节点 B 在删除时从未见过这个标签，因此不会删除它。合并之后 `("x", tag_2)` 就保留了下来。**最终效果是添加操作优先。**

可以打一个比方：就像快递单号一样，每次寄包裹都生成一个唯一的快递单号。如果你说"取消我寄的那个包裹"，你只能取消你目前知道单号的那些包裹。如果对方同时又寄了一个新包裹（新单号），你不知道这个新单号，自然也取消不了它。

```json
Request:  {"type": "or_set_add", "msg_id": 1, "element": "apple"}
Response: {"type": "or_set_add_ok", "in_reply_to": 1, "tag": "uuid-001"}

Request:  {"type": "or_set_remove", "msg_id": 2, "element": "apple"}
Response: {"type": "or_set_remove_ok", "in_reply_to": 2, "tags_removed": ["uuid-001"]}

Request:  {"type": "or_set_read", "msg_id": 3}
Response: {"type": "or_set_read_ok", "in_reply_to": 3, "elements": ["banana", "cherry"]}
```

## 涉及概念

- OR-Set
- observed-remove
- unique tags
- add-wins semantics
- concurrent remove

## 实现提示

- 每次添加元素时都要生成一个唯一标签（比如使用 UUID）
- 添加操作创建一条新记录：（元素, 唯一标签）
- 删除操作移除该元素当前所有已知的（元素, 标签）记录
- 并发场景下的添加和删除：新添加产生的标签不在删除操作的已知范围内，因此不会被移除
- 合并两个副本时，取所有（元素, 标签）记录的并集

## 测试用例

### 1. 添加并读取元素

验证：读取结果中应包含 "apple"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"or_set_add","msg_id":2,"element":"apple"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 删除操作移除元素

验证：删除 "banana" 之后，读取结果中不应包含 "banana"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"or_set_add","msg_id":2,"element":"banana"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_remove","msg_id":3,"element":"banana"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [OR-Set CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#OR-Set)：维基百科上关于观察-删除集合的介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
