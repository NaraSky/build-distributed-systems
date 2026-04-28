# 基于向量时钟的键值存储冲突检测

英文标题：Vector Clock Conflict Detection in Key-Value Store
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-5-vc-conflict-kv>

课程：2. 标识符：分布式唯一 ID
任务序号：15
短标题：向量时钟冲突检测
难度：高级
子主题：Logical Clocks as IDs

## 中文导读

在真实的分布式数据库中，当两个客户端同时修改同一个数据却互相不知道对方的修改时，就会产生写冲突。本题要求你实现一个带有向量时钟冲突检测的键值存储，这正是 Riak 等数据库处理并发写入的核心机制。理解这个概念对掌握分布式数据一致性至关重要。

## 题目说明

在 Riak 等分布式数据库中，向量时钟被用来检测**写冲突**。当两个客户端同时对同一个键进行写入（彼此不知道对方的写入操作），数据库不会悄悄丢弃其中一个值，而是将两个值都保存下来，称为**兄弟值**（Siblings）。

打个比方：两个人同时编辑同一份文档的同一段话，一个改成了版本 A，另一个改成了版本 B。由于他们各自独立修改，系统无法自动判断哪个版本是正确的，所以两个版本都保留，等待后续解决。

实现一个基于向量时钟冲突检测的键值存储：

```json
写入: {"type": "vc_write", "msg_id": 1, "key": "x", "value": "a", "context": {"n1": 0}}
读取: {"type": "vc_read", "msg_id": 2, "key": "x"}
```

只有一个值时的读取响应：
```json
{"type": "vc_read_ok", "values": [{"value": "a", "vc": {"n1": 1}}], "siblings": 1}
```

发生并发写入冲突后的读取响应：
```json
{"type": "vc_read_ok", "values": [
    {"value": "a", "vc": {"n1": 1}},
    {"value": "b", "vc": {"n2": 1}}
], "siblings": 2}
```

## 涉及概念

- `conflict detection`
- `key-value store`
- `sibling values`
- `last-writer-wins`

## 实现提示

- 每个键存储的值都需要搭配写入时的向量时钟
- 写入时，客户端需要提供它之前读取到的向量时钟（即上下文 context）
- 如果写入的向量时钟支配已存储的向量时钟，说明这是一次正常的更新覆盖
- 如果两个向量时钟是并发关系，则将两个值都作为兄弟值保存
- 读取时返回所有兄弟值及其对应的向量时钟

## 测试用例

### 1. 写入并读取单个值

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_write","msg_id":2,"key":"x","value":"hello","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"vc_read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_write_ok", "key": "x", "vc": {"c1": 1}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_read_ok", "values": [{"value": "hello", "vc": {"c1": 1}}], "siblings": 1, "in_reply_to": 3, "msg_id": 2}}
```

### 2. 读取不存在的键返回空结果

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_read","msg_id":2,"key":"missing"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_read_ok", "values": [], "siblings": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Dynamo: Amazon Highly Available Key-Value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：亚马逊 Dynamo 论文，描述了基于向量时钟的冲突解决机制

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
