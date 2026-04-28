# 实现 Scatter-Gather Search Across Shards

英文标题：Implement Scatter-Gather Search Across Shards
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-3-scatter-gather>

课程：23. 搜索器：分布式搜索
任务序号：8
短标题：Scatter-Gather
难度：advanced
子主题：Distributed Sharding和复制

## 中文导读

本题要求你完成 `实现 Scatter-Gather Search Across Shards`。

重点关注：`scatter-gather`、`distributed search`、`local top-K`、`global merge`、`re-ranking`。

建议先按提示逐步实现：Coordinator sends the search query to ALL shards in parallel。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Distributed search uses the scatter-gather pattern: the coordinator broadcasts the query to ALL shards, each returns local results,和the coordinator merges them.

**Scatter-gather flow**:
1. 客户端 sends search to coordinator: `{"query": {...}, "size": 10}`
2. Coordinator sends the query to all N shards in parallel (scatter)
3. Each 分片 runs the query against its local inverted 索引
4. Each 分片 returns its top-10 results，包含scores (local top-K)
5. Coordinator receives N lists of 10 results = N*10 candidates
6. Coordinator sorts all candidates by score和takes the global top 10 (gather)

**Deep pagination problem**:用于`from=1000, size=10`, each 分片 must return 1010 results. With 5 shards, the coordinator processes 5050 documents. This is why deep pagination is expensive.

```JSON
请求:  {"type": "search", "msg_id": 1, "索引": "articles", "query": {"match": {"title": "distributed"}}, "size": 10}
响应: {"type": "search_ok", "in_reply_to": 1, "hits": {"total": 42, "hits": [...]}, "shards": {"total": 5, "successful": 5, "failed": 0}}
```

## 涉及概念

- `scatter-gather`
- `distributed search`
- `local top-K`
- `global merge`
- `re-ranking`

## 实现提示

- Coordinator sends the search query to ALL shards in parallel
- Each 分片 runs the query against its local inverted 索引和returns top-K results
- Coordinator merges all local top-K lists into a global top-K by re-ranking
- K at the 分片 level must be >= K at the global level用于correctness
- Pagination: use "from"和"size" parameters. Each 分片 returns from+size results.

## 测试用例

### 1. Search queries all shards

search_ok shards.total should match the number of shards in the 索引.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":2,"index":"articles","query":{"match":{"title":"test"}},"size":10}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Results are sorted by score globally

Hits should be sorted by _score descending (global ranking, not per-分片).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":2,"index":"idx","query":{"match":{"title":"distributed"}},"size":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Distributed Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-shard-routing.html)：Elasticsearch documentation on distributed search execution

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
