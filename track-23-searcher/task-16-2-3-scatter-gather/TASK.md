# Implement Scatter-Gather Search Across Shards

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-3-scatter-gather>

Track: 23. The Searcher
Task order: 8
Short title: Scatter-Gather
Difficulty: advanced
Subtrack: Distributed Sharding and Replication

## Problem

Distributed search uses the scatter-gather pattern: the coordinator broadcasts the query to ALL shards, each returns local results, and the coordinator merges them.

**Scatter-gather flow**:
1. Client sends search to coordinator: `{"query": {...}, "size": 10}`
2. Coordinator sends the query to all N shards in parallel (scatter)
3. Each shard runs the query against its local inverted index
4. Each shard returns its top-10 results with scores (local top-K)
5. Coordinator receives N lists of 10 results = N*10 candidates
6. Coordinator sorts all candidates by score and takes the global top 10 (gather)

**Deep pagination problem**: for `from=1000, size=10`, each shard must return 1010 results. With 5 shards, the coordinator processes 5050 documents. This is why deep pagination is expensive.

```json
Request:  {"type": "search", "msg_id": 1, "index": "articles", "query": {"match": {"title": "distributed"}}, "size": 10}
Response: {"type": "search_ok", "in_reply_to": 1, "hits": {"total": 42, "hits": [...]}, "shards": {"total": 5, "successful": 5, "failed": 0}}
```

## Concepts

- scatter-gather
- distributed search
- local top-K
- global merge
- re-ranking

## Hints

- Coordinator sends the search query to ALL shards in parallel
- Each shard runs the query against its local inverted index and returns top-K results
- Coordinator merges all local top-K lists into a global top-K by re-ranking
- K at the shard level must be >= K at the global level for correctness
- Pagination: use "from" and "size" parameters. Each shard returns from+size results.

## Test Cases

### 1. Search queries all shards

search_ok shards.total should match the number of shards in the index.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":2,"index":"articles","query":{"match":{"title":"test"}},"size":10}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Results are sorted by score globally

Hits should be sorted by _score descending (global ranking, not per-shard).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":2,"index":"idx","query":{"match":{"title":"distributed"}},"size":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Distributed Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-shard-routing.html): Elasticsearch documentation on distributed search execution

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
