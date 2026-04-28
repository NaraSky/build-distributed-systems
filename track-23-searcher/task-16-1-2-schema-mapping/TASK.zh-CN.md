# 实现字段类型的模式映射

英文标题：Implement Schema Mapping with Field Types
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-2-schema-mapping>

课程：23. 搜索引擎
任务序号：2
短标题：模式映射
难度：进阶
子主题：文档模型与映射

## 中文导读

这道题要求你为索引中的每个字段定义类型映射（Schema Mapping），比如哪些字段是文本、哪些是数字。字段类型决定了数据如何被索引和搜索，是搜索引擎正确工作的关键配置。

## 题目说明

模式映射（Schema Mapping）定义了索引中各个字段的类型。每个字段的类型决定了它被索引和搜索的方式。

**字段类型**：
- `text`：经过分析处理，用于全文搜索。值会被分词（拆成一个个单词）、转为小写并进行词干提取。搜索时匹配的是单个词元。
- `keyword`：不做分析处理，原样存储。适用于精确匹配、排序和聚合，适合存储标识符、标签和枚举值。
- `integer`：数值类型，支持范围查询和排序。
- `date`：日期时间类型，内部以毫秒级时间戳存储。

**映射示例**：
```json
{"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}, "created_at": {"type": "date"}}}
```

```json
Request:  {"type": "mapping_put", "msg_id": 1, "index": "articles", "mapping": {"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}}}}
Response: {"type": "mapping_put_ok", "in_reply_to": 1, "index": "articles", "fields": 3}

Request:  {"type": "mapping_get", "msg_id": 2, "index": "articles"}
Response: {"type": "mapping_get_ok", "in_reply_to": 2, "mapping": {"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}}}}
```

## 涉及概念

- schema mapping
- field types
- text tokenization
- keyword field
- type inference

## 实现提示

- 定义字段类型：`text`（分词后用于全文搜索）、`keyword`（精确匹配）、`integer`、`date`
- `text` 类型的字段会被分析器拆分成词元（下一个任务会详细介绍）
- `keyword` 类型的字段原样索引，用于精确匹配、过滤和聚合
- 映射按索引定义，同一个索引中的所有文档共用同一套映射
- 如果出现类型冲突（比如字段 `"age"` 在一个文档中是文本，在另一个中是整数），必须拒绝

## 测试用例

### 1. 创建并获取映射

`mapping_get_ok` 应返回包含 `title`（text 类型）和 `status`（keyword 类型）的映射。

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

### 2. 索引字段类型正确的文档应成功

索引一个包含整数字段且与映射匹配的文档应当成功。

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

- [Elasticsearch Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)：关于字段映射和类型的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
