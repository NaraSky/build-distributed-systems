# 实现文档存储

英文标题：Implement a JSON Document Store
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-1-document-store>

课程：23. 搜索引擎
任务序号：1
短标题：文档存储
难度：进阶
子主题：文档模型与映射

## 中文导读

这道题要求你实现一个最基础的文档存储（Document Store），支持对文档的增删查操作。文档存储是搜索引擎的地基，所有后续的索引、搜索功能都建立在它之上。理解文档的存储和检索方式，是构建搜索引擎的第一步。

## 题目说明

搜索引擎的基础是文档存储（Document Store）。每个文档是一个任意结构的 JSON 对象，通过唯一的 UUID 来标识。

**核心操作**：
- `index(doc)`：存储一个 JSON 文档。如果文档中没有 `_id` 字段，则自动生成一个 UUID v4。返回 `_id` 和版本号。
- `get(id)`：根据 `_id` 检索文档。返回完整的 JSON 文档，包含元数据（`_id`、`_version`、`_source`）。
- `delete(id)`：将文档标记为已删除。返回操作是否成功。

**存储方式**：目前使用内存中的哈希表，或者简单的"一个文件存一个文档"的方式。每个文档以 JSON 格式存储，以 `_id` 作为键。

文档不要求固定的结构：任何合法的 JSON 都可以作为文档。字段类型可以自动推断，也可以显式映射（将在下一个任务中介绍）。

```json
Request:  {"type": "doc_index", "msg_id": 1, "doc": {"title": "Distributed Systems", "author": "Kleppmann", "year": 2017}}
Response: {"type": "doc_index_ok", "in_reply_to": 1, "_id": "a1b2c3d4", "_version": 1, "result": "created"}

Request:  {"type": "doc_get", "msg_id": 2, "_id": "a1b2c3d4"}
Response: {"type": "doc_get_ok", "in_reply_to": 2, "_id": "a1b2c3d4", "_source": {"title": "Distributed Systems", "author": "Kleppmann", "year": 2017}}
```

## 涉及概念

- document store
- JSON document
- UUID primary key
- index operation
- CRUD

## 实现提示

- 每个文档是一个 JSON 对象，系统会为它分配一个 `_id` 字段（UUID v4 格式）
- `index(doc)` 用于存储文档，并返回分配的 `_id`
- `get(id)` 根据 `_id` 检索文档，如果不存在则返回空
- `delete(id)` 删除文档，并返回操作是否成功
- 使用简单的文件或哈希表来存储文档，以 `_id` 作为键

## 测试用例

### 1. 索引并检索文档

`doc_index_ok` 应返回一个合法的 `_id` 以及 `result` 为 `"created"`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"doc":{"title":"DS","author":"MK","year":2017}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 获取已索引的文档

`doc_get_ok` 应在 `_source` 中返回之前存入的同一份文档。

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

- [Elasticsearch Document API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html)：关于文档增删改查接口的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
