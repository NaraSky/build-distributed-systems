# 实现最后写入者胜出的键值存储

英文标题：Implement Last-Writer-Wins Key-Value Store
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-3-lww-kv>

课程：3. 传播者：Gossip 信息传播
任务序号：18
短标题：最后写入者胜出键值存储
难度：高级
子主题：Epidemic Algorithms and CRDT Gossip

## 中文导读

这道题让你实现一个"最后写入者胜出"（LWW）的键值存储。当多个节点同时写入同一个键时，系统通过比较时间戳来决定保留哪个值——时间戳更大的胜出。这种策略实现简单，但代价是可能悄悄丢失并发写入的数据。理解它的优缺点，是后续学习更高级冲突解决方案的前提。

## 题目说明

**最后写入者胜出（LWW）** 寄存器通过始终保留时间戳最新的值来解决冲突。这种方式简单直接，但可能会丢失并发写入的数据。

你需要实现一个基于此策略的键值存储：

```json
请求:  {"type": "write", "msg_id": 1, "key": "x", "value": "hello"}
响应: {"type": "write_ok", "in_reply_to": 1, "ts": 1704067200.123}

请求:  {"type": "kv_read", "msg_id": 2, "key": "x"}
响应: {"type": "kv_read_ok", "in_reply_to": 2, "key": "x", "value": "hello", "ts": 1704067200.123}

请求:  {"type": "kv_merge", "msg_id": 3, "entries": {"x": {"value": "world", "ts": 1704067201.0}}}
响应: {"type": "kv_merge_ok", "in_reply_to": 3, "updated": 1}
```

## 涉及概念

- `LWW register`
- `conflict resolution`
- `timestamp ordering`
- `gossip replication`

## 实现提示

- 每个值都会配对一个写入时的时间戳
- 合并时，保留时间戳更大的那个值
- 如果时间戳相同，使用确定性的决胜规则（比如比较节点编号）
- 该策略虽然简单，但会悄悄丢失并发写入的数据
- 使用 `System.currentTimeMillis()` 或类似方法获取时间戳

## 测试用例

### 1. 写入后读取

验证：写入成功返回时间戳，随后读取返回正确的值。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"write","msg_id":2,"key":"x","value":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"kv_read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 读取不存在的键返回错误

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_read","msg_id":2,"key":"missing"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "error", "code": 20, "text": "Key not found", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Last-Writer-Wins Register](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#LWW-Element-Set)：维基百科上关于最后写入者胜出 CRDT 语义的介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
