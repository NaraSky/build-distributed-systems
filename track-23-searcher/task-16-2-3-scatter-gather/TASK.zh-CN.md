# 实现跨分片的分散-聚合搜索

英文标题：Implement Scatter-Gather Search Across Shards
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-3-scatter-gather>

课程：23. 搜索引擎
任务序号：8
短标题：分散-聚合
难度：高级
子主题：分布式分片与复制

## 中文导读

这道题要求你实现分散-聚合（Scatter-Gather）搜索模式：协调节点把查询广播给所有分片，各分片返回本地结果，最后由协调节点汇总排序。这是分布式搜索引擎的核心查询执行方式，理解它有助于明白为什么深度翻页会很慢。

## 题目说明

分布式搜索使用分散-聚合（Scatter-Gather）模式：协调节点将查询广播到所有分片，每个分片返回本地结果，协调节点再进行合并。

**分散-聚合流程**：
1. 客户端向协调节点发送搜索请求：`{"query": {...}, "size": 10}`
2. 协调节点将查询并行发送到所有 N 个分片（分散阶段）
3. 每个分片在本地倒排索引上执行查询
4. 每个分片返回自己的前 10 条结果及分数（本地前 K 名）
5. 协调节点收到 N 个列表，共 N*10 条候选结果
6. 协调节点按分数对所有候选结果排序，取全局前 10 条（聚合阶段）

**深度翻页问题**：假设请求 `from=1000, size=10`，每个分片需要返回 1010 条结果。如果有 5 个分片，协调节点就要处理 5050 条文档。这就是深度翻页开销大的原因。

```json
Request:  {"type": "search", "msg_id": 1, "index": "articles", "query": {"match": {"title": "distributed"}}, "size": 10}
Response: {"type": "search_ok", "in_reply_to": 1, "hits": {"total": 42, "hits": [...]}, "shards": {"total": 5, "successful": 5, "failed": 0}}
```

## 涉及概念

- scatter-gather
- distributed search
- local top-K
- global merge
- re-ranking

## 实现提示

- 协调节点将搜索查询并行发送到所有分片
- 每个分片在本地倒排索引上执行查询，返回前 K 条结果
- 协调节点将各分片的本地前 K 列表合并为全局前 K，重新排序
- 分片级别的 K 必须大于或等于全局级别的 K，才能保证结果正确
- 翻页：使用 `from` 和 `size` 参数。每个分片需要返回 `from + size` 条结果

## 测试用例

### 1. 搜索查询发送到所有分片

`search_ok` 中的 `shards.total` 应与索引中的分片数量一致。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":2,"index":"articles","query":{"match":{"title":"test"}},"size":10}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 结果按全局分数排序

搜索结果应按 `_score` 降序排列（全局排名，而非单个分片内的排名）。

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

- [Elasticsearch Distributed Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-shard-routing.html)：关于分布式搜索执行流程的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
