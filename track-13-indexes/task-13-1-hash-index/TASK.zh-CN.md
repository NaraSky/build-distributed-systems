# 实现 Hash 索引

英文标题：Implement Hash Index
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-1-hash-index>

课程：13. 索引
任务序号：1
短标题：Hash 索引
难度：intermediate

## 中文导读

本题要求你完成 `实现 Hash 索引`。

重点关注：`indexing`、`hash table`、`O(1) lookup`。

建议先按提示逐步实现：Map keys to data locations。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a hash 索引 that maps keys to data file offsets:

1. Hash each key to a bucket
2. Store key和file offset in the bucket
3. Lookup returns the offset用于a key
4.处理collisions，包含chaining or probing

Hash indexes provide O(1) point lookups but cannot support range queries.

## 概念说明

### Why Indexing?

Without indexes, finding a record requires scanning all data - O(n) cost. Indexes provide shortcuts from keys to locations, reducing lookup to O(1)用于hash or O(日志 n)用于tree indexes.

### Hash 索引

Hash indexes map key -> file offset. They are extremely fast用于exact matches. Bitcask, a 日志-structured store, uses hash indexes. The tradeoff: 索引 must fit in memory,和no range queries.

## 涉及概念

- `indexing`
- `hash table`
- `O(1) lookup`

## 实现提示

- Map keys to data locations
-处理hash collisions
- Support insert, lookup, delete

## 测试用例

### 1. Insert和lookup

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"index_put","msg_id":2,"key":"foo","value":100}}
{"src":"c2","dest":"n1","body":{"type":"index_get","msg_id":3,"key":"foo"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"index_put_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"index_get_ok","in_reply_to":3,"msg_id":2,"value":100}}
```

## 参考资料

- [DDIA Chapter 3](https://dataintensive.net/)：存储和Retrieval chapter on 日志-structured 存储

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
