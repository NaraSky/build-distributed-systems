# Implement a Full-Text Search API

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-5-search-api>

Track: 23. The Searcher
Task order: 5
Short title: Search API
Difficulty: intermediate
Subtrack: Document Model and Mapping

## Problem

The search API accepts a structured query, looks up the inverted index, and returns matching documents ranked by relevance.

**Match query**: the most common query type. Analyzes the input text and matches against the inverted index.
```json
{"query": {"match": {"title": "distributed systems"}}}
```
This is analyzed to tokens ["distribut", "system"] and matched against the inverted index for the "title" field.

**Scoring**: documents are ranked by relevance. A simple scoring function: `score = number of matching terms / total query terms`. More sophisticated scoring uses TF-IDF or BM25.

**Boolean queries**: combine multiple conditions with must (AND), should (OR), and must_not (NOT).

```json
Request:  {"type": "search", "msg_id": 1, "index": "articles", "query": {"match": {"title": "distributed systems"}}}
Response: {"type": "search_ok", "in_reply_to": 1, "hits": {"total": 2, "hits": [{"_id": "a1", "_score": 0.95, "_source": {"title": "Distributed Systems Primer"}}, {"_id": "b2", "_score": 0.7, "_source": {"title": "Operating Systems"}}]}}
```

## Concepts

- search API
- match query
- inverted index lookup
- relevance scoring
- boolean query

## Hints

- Parse the match query to extract the field and search terms
- Analyze the search terms using the same analyzer as index time
- Look up each term in the inverted index to find matching document IDs
- For multi-term queries, intersect (AND) or union (OR) the posting lists
- Return matching documents sorted by relevance (number of matching terms)

## Test Cases

### 1. Match query returns relevant docs

search_ok hits should include the indexed document.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"books","doc":{"title":"Distributed Systems"}}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":3,"index":"books","query":{"match":{"title":"distributed"}}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Search non-matching term returns empty

search_ok hits.total should be 0 for non-matching query.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"search","msg_id":2,"index":"books","query":{"match":{"title":"quantum physics"}}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html): Elasticsearch documentation on the Search API and query DSL

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
