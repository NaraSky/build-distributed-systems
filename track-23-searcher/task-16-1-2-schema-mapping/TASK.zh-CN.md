# 实现 Schema Mapping，包含Field Types

英文标题：Implement Schema Mapping，包含Field Types
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-2-schema-mapping>

课程：23. 搜索器：分布式搜索
任务序号：2
短标题：Schema Mapping
难度：intermediate
子主题：Document模式l和Mapping

## 中文导读

本题要求你完成 `实现 Schema Mapping，包含Field Types`。

重点关注：`schema mapping`、`field types`、`text tokenization`、`keyword field`、`type inference`。

建议先按提示逐步实现：Define field types: text (tokenized用于full-text search), keyword (exact match), integer, date。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Schema mapping defines the field types in your 索引. Each field has a type that determines how it is indexed和searched.

**Field types**:
- `text`: analyzed用于full-text search. The value is tokenized (split into words), lowercased,和stemmed. Searches match individual tokens.
- `keyword`: not analyzed. Indexed as-is用于exact matching, sorting,和aggregation. Good用于IDs, tags,和enum values.
- `integer`: numeric type用于range queries和sorting.
- `date`: date/time type, stored as epoch milliseconds internally.

**Mapping example**:
```JSON
{"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}, "created_at": {"type": "date"}}}
```

```JSON
请求:  {"type": "mapping_put", "msg_id": 1, "索引": "articles", "mapping": {"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}}}}
响应: {"type": "mapping_put_ok", "in_reply_to": 1, "索引": "articles", "fields": 3}

请求:  {"type": "mapping_get", "msg_id": 2, "索引": "articles"}
响应: {"type": "mapping_get_ok", "in_reply_to": 2, "mapping": {"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}}}}
```

## 涉及概念

- `schema mapping`
- `field types`
- `text tokenization`
- `keyword field`
- `type inference`

## 实现提示

- Define field types: text (tokenized用于full-text search), keyword (exact match), integer, date
- Text fields are split into tokens by an analyzer (covered in the next task)
- Keyword fields are indexed as-is用于exact matching, filtering,和aggregation
- Mapping is defined per-索引和applies to all documents in that 索引
- Type conflicts (e.g., field "age" as text in one doc和integer in another) must be rejected

## 测试用例

### 1. 创建和retrieve mapping

mapping_get_ok should return the mapping，包含title (text)和status (keyword).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mapping_put","msg_id":2,"index":"articles","mapping":{"properties":{"title":{"type":"text"},"status":{"type":"keyword"}}}}}
{"src":"c1","dest":"n1","body":{"type":"mapping_get","msg_id":3,"index":"articles"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 索引 doc，包含correct field types succeeds

Indexing a doc，包含integer field matching the mapping should succeed.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mapping_put","msg_id":2,"index":"articles","mapping":{"properties":{"views":{"type":"integer"}}}}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":3,"index":"articles","doc":{"views":42}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)：Elasticsearch documentation on field mappings和types

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
