# Implement Dynamic Mapping with Type Auto-Detection

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-4-dynamic-mapping>

Track: 23. The Searcher
Task order: 4
Short title: Dynamic Mapping
Difficulty: intermediate
Subtrack: Document Model and Mapping

## Problem

Dynamic mapping automatically detects field types when new documents are indexed. This provides schema-on-write convenience but introduces risks.

**Auto-detection rules**:
- String -> `text` with a `keyword` sub-field
- Integer -> `long`
- Decimal -> `double`
- Boolean -> `boolean`
- Object -> `object` (nested mapping)
- Array -> type of the first element

**Risks**:
1. **Mapping explosion**: if documents have thousands of unique field names (e.g., user-generated keys), the mapping grows unboundedly, consuming memory and degrading performance.
2. **Type conflicts**: field "price" in doc1 is "10" (string), in doc2 is 10 (integer). The second document fails to index.

```json
Request:  {"type": "doc_index", "msg_id": 1, "index": "logs", "doc": {"message": "error occurred", "level": "ERROR", "status_code": 500, "success": false}}
Response: {"type": "doc_index_ok", "in_reply_to": 1, "_id": "abc", "dynamic_fields_added": [{"name": "message", "type": "text"}, {"name": "level", "type": "text"}, {"name": "status_code", "type": "long"}, {"name": "success", "type": "boolean"}]}
```

## Concepts

- dynamic mapping
- type auto-detection
- mapping explosion
- type conflict
- schema-on-read

## Hints

- When a field is first seen, auto-detect its type from the JSON value
- String values default to "text" with a "keyword" sub-field
- Number values (no decimal) default to "long", with decimal to "double"
- Boolean values map to "boolean", objects create nested mappings
- Risk: mapping explosion when documents have many unique field names (thousands of fields)

## Test Cases

### 1. Dynamic mapping auto-detects string as text

mapping_get_ok should show "message" field with type "text".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"logs","doc":{"message":"hello"}}}
{"src":"c1","dest":"n1","body":{"type":"mapping_get","msg_id":3,"index":"logs"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Dynamic mapping detects integer as long

mapping_get_ok should show "count" field with type "long".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"metrics","doc":{"count":42}}}
{"src":"c1","dest":"n1","body":{"type":"mapping_get","msg_id":3,"index":"metrics"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Dynamic Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-mapping.html): Elasticsearch documentation on dynamic mapping and type auto-detection

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
