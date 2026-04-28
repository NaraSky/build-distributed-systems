# 实现 a Full-Text Search API

英文标题：Implement a Full-Text Search API
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-5-search-api>

课程：23. 搜索器：分布式搜索
任务序号：5
短标题：Search API
难度：intermediate
子主题：Document模式l和Mapping

## 中文导读

本题要求你完成 `实现 a Full-Text Search API`。

重点关注：`search API`、`match query`、`inverted index lookup`、`relevance scoring`、`boolean query`。

建议先按提示逐步实现：Parse the match query to extract the field和search terms。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The search API accepts a structured query, looks up the inverted 索引,和returns matching documents ranked by relevance.

**Match query**: the most common query type. Analyzes the input text和matches against the inverted 索引.
```JSON
{"query": {"match": {"title": "分布式系统"}}}
```
This is analyzed to tokens ["distribut", "system"]和matched against the inverted 索引用于the "title" field.

**Scoring**: documents are ranked by relevance. A simple scoring function: `score = number of matching terms / total query terms`. More sophisticated scoring uses TF-IDF or BM25.

**Boolean queries**: combine multiple conditions，包含must (AND), should (OR),和must_not (NOT).

```JSON
请求:  {"type": "search", "msg_id": 1, "索引": "articles", "query": {"match": {"title": "分布式系统"}}}
响应: {"type": "search_ok", "in_reply_to": 1, "hits": {"total": 2, "hits": [{"_id": "a1", "_score": 0.95, "_source": {"title": "分布式系统 Primer"}}, {"_id": "b2", "_score": 0.7, "_source": {"title": "Operating Systems"}}]}}
```

## 涉及概念

- `search API`
- `match query`
- `inverted index lookup`
- `relevance scoring`
- `boolean query`

## 实现提示

- Parse the match query to extract the field和search terms
- Analyze the search terms使用the same analyzer as 索引 time
- Look up each term in the inverted 索引 to find matching document IDs
- For multi-term queries, intersect (AND) or union (OR) the posting lists
- Return matching documents sorted by relevance (number of matching terms)

## 测试用例

### 1. Match query returns relevant docs

search_ok hits should include the indexed document.

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

### 2. Search non-matching term returns empty

search_ok hits.total should be 0用于non-matching query.

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

- [Elasticsearch Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html)：Elasticsearch documentation on the Search API和query DSL

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
