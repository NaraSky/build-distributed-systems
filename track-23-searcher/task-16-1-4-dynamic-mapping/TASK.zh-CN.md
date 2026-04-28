# 实现 Dynamic Mapping，包含Type Auto-Detection

英文标题：Implement Dynamic Mapping，包含Type Auto-Detection
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-4-dynamic-mapping>

课程：23. 搜索器：分布式搜索
任务序号：4
短标题：Dynamic Mapping
难度：intermediate
子主题：Document模式l和Mapping

## 中文导读

本题要求你完成 `实现 Dynamic Mapping，包含Type Auto-Detection`。

重点关注：`dynamic mapping`、`type auto-detection`、`mapping explosion`、`type conflict`、`schema-on-read`。

建议先按提示逐步实现：When a field is first seen, auto-detect its type from the JSON value。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Dynamic mapping automatically detects field types when new documents are indexed. This provides schema-on-write convenience but introduces risks.

**Auto-detection rules**:
- String -> `text`，包含a `keyword` sub-field
- Integer -> `long`
- Decimal -> `double`
- Boolean -> `boolean`
- Object -> `object` (nested mapping)
- Array -> type of the first element

**Risks**:
1. **Mapping explosion**: if documents have thousands of unique field names (e.g., user-generated keys), the mapping grows unboundedly, consuming memory和degrading performance.
2. **Type conflicts**: field "price" in doc1 is "10" (string), in doc2 is 10 (integer). The second document fails to 索引.

```JSON
请求:  {"type": "doc_index", "msg_id": 1, "索引": "logs", "doc": {"消息": "error occurred", "level": "ERROR", "status_code": 500, "success": false}}
响应: {"type": "doc_index_ok", "in_reply_to": 1, "_id": "abc", "dynamic_fields_added": [{"name": "消息", "type": "text"}, {"name": "level", "type": "text"}, {"name": "status_code", "type": "long"}, {"name": "success", "type": "boolean"}]}
```

## 涉及概念

- `dynamic mapping`
- `type auto-detection`
- `mapping explosion`
- `type conflict`
- `schema-on-read`

## 实现提示

- When a field is first seen, auto-detect its type from the JSON value
- String values default to "text"，包含a "keyword" sub-field
- Number values (no decimal) default to "long",，包含decimal to "double"
- Boolean values map to "boolean", objects create nested mappings
- Risk: mapping explosion when documents have many unique field names (thousands of fields)

## 测试用例

### 1. Dynamic mapping auto-detects string as text

mapping_get_ok should show "消息" field，包含type "text".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"logs","doc":{"message":"hello"}}}
{"src":"c1","dest":"n1","body":{"type":"mapping_get","msg_id":3,"index":"logs"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Dynamic mapping detects integer as long

mapping_get_ok should show "count" field，包含type "long".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"metrics","doc":{"count":42}}}
{"src":"c1","dest":"n1","body":{"type":"mapping_get","msg_id":3,"index":"metrics"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Dynamic Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-mapping.html)：Elasticsearch documentation on dynamic mapping和type auto-detection

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
