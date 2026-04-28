# 实现 a JSON Document 存储

英文标题：Implement a JSON Document Store
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-1-document-store>

课程：23. 搜索器：分布式搜索
任务序号：1
短标题：Document 存储
难度：intermediate
子主题：Document模式l和Mapping

## 中文导读

本题要求你完成 `实现 a JSON Document 存储`。

重点关注：`document store`、`JSON document`、`UUID primary key`、`index operation`、`CRUD`。

建议先按提示逐步实现：Each document is a JSON object，包含a system-assigned "_id" field (UUID v4)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The foundation of a search engine is the document store. Each document is a JSON object，包含arbitrary fields, identified by a unique UUID.

**Core operations**:
- `索引(doc)`: store a JSON document. If no `_id` is provided, generate a UUID v4. Return the `_id`和a version number.
- `get(id)`: retrieve the document by its `_id`. Return the full JSON document including 元数据 (`_id`, `_version`, `_source`).
- `delete(id)`: mark the document as deleted. Return success/故障.

**存储**:用于now, use an in-memory hash map or a simple file-per-document store. Each document is stored as a JSON blob keyed by `_id`.

Documents are schema-free: any JSON structure is valid. Field types are inferred or explicitly mapped (covered in the next task).

```JSON
请求:  {"type": "doc_index", "msg_id": 1, "doc": {"title": "分布式系统", "author": "Kleppmann", "year": 2017}}
响应: {"type": "doc_index_ok", "in_reply_to": 1, "_id": "a1b2c3d4", "_version": 1, "result": "created"}

请求:  {"type": "doc_get", "msg_id": 2, "_id": "a1b2c3d4"}
响应: {"type": "doc_get_ok", "in_reply_to": 2, "_id": "a1b2c3d4", "_source": {"title": "分布式系统", "author": "Kleppmann", "year": 2017}}
```

## 涉及概念

- `document store`
- `JSON document`
- `UUID primary key`
- `index operation`
- `CRUD`

## 实现提示

- Each document is a JSON object，包含a system-assigned "_id" field (UUID v4)
- 索引(doc) stores the document和returns the assigned _id
- get(id) retrieves the document by _id, returning null if not found
- delete(id) removes the document和returns success/故障
- Store documents in a simple file or hash map keyed by _id

## 测试用例

### 1. 索引和retrieve a document

doc_index_ok should return a valid _id和result "created".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"doc":{"title":"DS","author":"MK","year":2017}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Get returns indexed document

doc_get_ok should return the same document in _source.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"doc":{"k":"v"}}}
{"src":"c1","dest":"n1","body":{"type":"doc_get","msg_id":3,"_id":"LAST_ID"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Document API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html)：Elasticsearch documentation on the Document API

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
