# 实现全文搜索接口

英文标题：Implement a Full-Text Search API
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-5-search-api>

课程：23. 搜索引擎
任务序号：5
短标题：搜索接口
难度：进阶
子主题：文档模型与映射

## 中文导读

这道题要求你实现一个全文搜索接口（Search API），它接收结构化查询、查找倒排索引，并按相关性返回匹配的文档。搜索接口是用户真正使用搜索引擎的入口，把前几个任务中构建的文档存储、映射和文本分析串联起来。

## 题目说明

搜索接口（Search API）接收一个结构化的查询，查找倒排索引（Inverted Index），并按相关性排序返回匹配的文档。

**匹配查询（Match Query）**：最常用的查询类型。对输入文本进行分析处理，然后在倒排索引中查找匹配项。
```json
{"query": {"match": {"title": "distributed systems"}}}
```
这段查询会被分析为词元 `["distribut", "system"]`，然后在 `"title"` 字段的倒排索引中进行匹配。

**评分（Scoring）**：文档按相关性排序。一个简单的评分函数是：`分数 = 匹配的词数 / 查询总词数`。更精细的评分可以使用 TF-IDF 或 BM25 算法。

**布尔查询（Boolean Query）**：通过 `must`（与）、`should`（或）、`must_not`（非）组合多个条件。

```json
Request:  {"type": "search", "msg_id": 1, "index": "articles", "query": {"match": {"title": "distributed systems"}}}
Response: {"type": "search_ok", "in_reply_to": 1, "hits": {"total": 2, "hits": [{"_id": "a1", "_score": 0.95, "_source": {"title": "Distributed Systems Primer"}}, {"_id": "b2", "_score": 0.7, "_source": {"title": "Operating Systems"}}]}}
```

## 涉及概念

- search API
- match query
- inverted index lookup
- relevance scoring
- boolean query

## 实现提示

- 解析匹配查询，提取目标字段和搜索词
- 使用与索引时相同的分析器来分析搜索词
- 在倒排索引中查找每个词元，找到匹配的文档编号
- 对于多词查询，对倒排列表取交集（与操作）或取并集（或操作）
- 返回按相关性排序的匹配文档（按匹配词数排序）

## 测试用例

### 1. 匹配查询返回相关文档

`search_ok` 的结果中应包含之前索引的文档。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"books","doc":{"title":"Distributed Systems"}}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":3,"index":"books","query":{"match":{"title":"distributed"}}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 搜索不匹配的词应返回空结果

当查询词不匹配任何文档时，`search_ok` 中的 `hits.total` 应为 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":2,"index":"books","query":{"match":{"title":"quantum physics"}}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html)：关于搜索接口和查询语法的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
