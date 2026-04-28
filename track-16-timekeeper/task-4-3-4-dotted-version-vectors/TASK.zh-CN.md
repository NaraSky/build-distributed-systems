# 实现点版本向量

英文标题：Implement Dotted Version Vectors
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-4-dotted-version-vectors>

课程：16. 时间守卫：逻辑时钟
任务序号：14
短标题：点版本向量
难度：高级
子主题：向量时钟

## 中文导读

本题要求你实现点版本向量（Dotted Version Vectors）。标准的向量时钟存在一个问题：存储开销会随着参与过的节点数量线性增长。点版本向量通过将"因果上下文"和"事件标记"分离，巧妙地解决了这个问题。这是数据库 Riak 实际采用的方案，理解它有助于你掌握实际工程中的版本管理技术。

## 题目说明

标准的向量时钟有一个 O(N) 的存储开销，N 是曾经参与过的节点数量，会不断增长。点版本向量（Dotted Version Vectors，简称 DVV）是 Riak 数据库采用的方案，它通过将**因果上下文**和**事件点**分离来解决这个问题。

一个 DVV 由两部分组成：
- **点（dot）**：`(node_id, counter)`——表示当前这个值所代表的那一个事件
- **版本向量（version_vector）**：因果上下文，记录这个点之前发生过的所有事件

请实现一个基于 DVV 的版本管理系统：

```json
Request:  {"type": "dvv_update", "msg_id": 1, "key": "x", "value": "hello", "context": {}}
Response: {"type": "dvv_update_ok", "in_reply_to": 1, "dot": ["n1", 1], "version_vector": {}}

Request:  {"type": "dvv_update", "msg_id": 2, "key": "x", "value": "world", "context": {"n1": 1}}
Response: {"type": "dvv_update_ok", "in_reply_to": 2, "dot": ["n1", 2], "version_vector": {"n1": 1}}

Request:  {"type": "dvv_get", "msg_id": 3, "key": "x"}
Response: {"type": "dvv_get_ok", "in_reply_to": 3, "values": [{"value": "world", "dot": ["n1", 2]}], "context": {"n1": 2}}
```

## 涉及概念

- `dotted version vectors`
- `space optimization`
- `version vectors`
- `Riak`

## 实现提示

- 标准的向量时钟会随着参与过的节点数量线性增长
- 点版本向量将因果上下文（版本向量）和事件点分开存储
- 一个点是一个 `(node_id, counter)` 对，代表单个事件
- 版本向量记录了这个点之前发生过的所有事情
- 这种分离使得可以裁剪旧条目而不影响正确性

## 测试用例

### 1. 首次写入创建一个点

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":2,"key":"x","value":"hello","context":{}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dvv_update_ok", "in_reply_to": 2, "dot": ["n1", 1], "version_vector": {}, "msg_id": 1}}
```

### 2. 带上下文的顺序更新会覆盖旧值

`dvv_get_ok` 应该只返回值 v2 及其点 [n1, 2]，因为 v1 已被上下文覆盖。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":2,"key":"x","value":"v1","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":3,"key":"x","value":"v2","context":{"n1":1}}}
{"src":"c1","dest":"n1","body":{"type":"dvv_get","msg_id":4,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Dotted Version Vectors - Riak Core Concepts](https://riak.com/posts/technical/vector-clocks-revisited-part-2-dotted-version-vectors/)：介绍 Riak 如何用点版本向量替代向量时钟以提升效率

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
