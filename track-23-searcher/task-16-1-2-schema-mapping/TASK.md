# Implement Schema Mapping with Field Types

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-2-schema-mapping>

Track: 23. The Searcher
Task order: 2
Short title: Schema Mapping
Difficulty: intermediate
Subtrack: Document Model and Mapping

## Problem

Schema mapping defines the field types in your index. Each field has a type that determines how it is indexed and searched.

**Field types**:
- `text`: analyzed for full-text search. The value is tokenized (split into words), lowercased, and stemmed. Searches match individual tokens.
- `keyword`: not analyzed. Indexed as-is for exact matching, sorting, and aggregation. Good for IDs, tags, and enum values.
- `integer`: numeric type for range queries and sorting.
- `date`: date/time type, stored as epoch milliseconds internally.

**Mapping example**:
```json
{"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}, "created_at": {"type": "date"}}}
```

```json
Request:  {"type": "mapping_put", "msg_id": 1, "index": "articles", "mapping": {"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}}}}
Response: {"type": "mapping_put_ok", "in_reply_to": 1, "index": "articles", "fields": 3}

Request:  {"type": "mapping_get", "msg_id": 2, "index": "articles"}
Response: {"type": "mapping_get_ok", "in_reply_to": 2, "mapping": {"properties": {"title": {"type": "text"}, "status": {"type": "keyword"}, "views": {"type": "integer"}}}}
```

## Concepts

- schema mapping
- field types
- text tokenization
- keyword field
- type inference

## Hints

- Define field types: text (tokenized for full-text search), keyword (exact match), integer, date
- Text fields are split into tokens by an analyzer (covered in the next task)
- Keyword fields are indexed as-is for exact matching, filtering, and aggregation
- Mapping is defined per-index and applies to all documents in that index
- Type conflicts (e.g., field "age" as text in one doc and integer in another) must be rejected

## Test Cases

### 1. Create and retrieve mapping

mapping_get_ok should return the mapping with title (text) and status (keyword).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mapping_put","msg_id":2,"index":"articles","mapping":{"properties":{"title":{"type":"text"},"status":{"type":"keyword"}}}}}
{"src":"c1","dest":"n1","body":{"type":"mapping_get","msg_id":3,"index":"articles"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Index doc with correct field types succeeds

Indexing a doc with integer field matching the mapping should succeed.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mapping_put","msg_id":2,"index":"articles","mapping":{"properties":{"views":{"type":"integer"}}}}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":3,"index":"articles","doc":{"views":42}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html): Elasticsearch documentation on field mappings and types

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
