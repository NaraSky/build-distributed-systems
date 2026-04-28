# 添加 Secondary Indexes

英文标题：Add Secondary Indexes
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-4-secondary-index>

课程：13. 索引
任务序号：4
短标题：Secondary 索引
难度：intermediate

## 中文导读

本题要求你完成 `添加 Secondary Indexes`。

重点关注：`secondary index`、`non-key lookup`、`inverted index`。

建议先按提示逐步实现：Secondary 索引 maps attribute to primary keys。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement secondary indexes用于non-key attributes:

1. Primary 索引: primary_key -> data
2. Secondary 索引: attribute_value -> list of primary_keys
3. Query by attribute: secondary lookup, then primary lookups
4. Keep secondary 索引 updated on all writes/deletes

Secondary indexes enable efficient queries on any attribute, not just the primary key.

## 概念说明

### Secondary Indexes

Primary indexes organize data by primary key. But what if you need to find users by email or orders by status? Secondary indexes provide alternative access paths用于these non-key queries.

### Implementation Approaches

1. Separate 索引 file mapping attribute -> primary keys. 2. Covering 索引 includes full record to avoid primary lookup. 3. Inverted 索引用于text search.

## 涉及概念

- `secondary index`
- `non-key lookup`
- `inverted index`

## 实现提示

- Secondary 索引 maps attribute to primary keys
- Update secondary 索引 on data changes
-处理one-to-many relationships

## 测试用例

### 1. Secondary 索引 lookup

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"db_insert","msg_id":2,"id":1,"name":"Alice","status":"active"}}
{"src":"c2","dest":"n1","body":{"type":"db_insert","msg_id":3,"id":2,"name":"Bob","status":"active"}}
{"src":"c3","dest":"n1","body":{"type":"db_query","msg_id":4,"field":"status","value":"active"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"db_insert_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"db_insert_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c3","body":{"type":"db_query_ok","in_reply_to":4,"msg_id":3,"results":[1,2]}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
