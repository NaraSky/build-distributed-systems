# Implement a JSON Document Store

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-1-1-document-store>

Track: 23. The Searcher
Task order: 1
Short title: Document Store
Difficulty: intermediate
Subtrack: Document Model and Mapping

## Problem

The foundation of a search engine is the document store. Each document is a JSON object with arbitrary fields, identified by a unique UUID.

**Core operations**:
- `index(doc)`: store a JSON document. If no `_id` is provided, generate a UUID v4. Return the `_id` and a version number.
- `get(id)`: retrieve the document by its `_id`. Return the full JSON document including metadata (`_id`, `_version`, `_source`).
- `delete(id)`: mark the document as deleted. Return success/failure.

**Storage**: for now, use an in-memory hash map or a simple file-per-document store. Each document is stored as a JSON blob keyed by `_id`.

Documents are schema-free: any JSON structure is valid. Field types are inferred or explicitly mapped (covered in the next task).

```json
Request:  {"type": "doc_index", "msg_id": 1, "doc": {"title": "Distributed Systems", "author": "Kleppmann", "year": 2017}}
Response: {"type": "doc_index_ok", "in_reply_to": 1, "_id": "a1b2c3d4", "_version": 1, "result": "created"}

Request:  {"type": "doc_get", "msg_id": 2, "_id": "a1b2c3d4"}
Response: {"type": "doc_get_ok", "in_reply_to": 2, "_id": "a1b2c3d4", "_source": {"title": "Distributed Systems", "author": "Kleppmann", "year": 2017}}
```

## Concepts

- document store
- JSON document
- UUID primary key
- index operation
- CRUD

## Hints

- Each document is a JSON object with a system-assigned "_id" field (UUID v4)
- index(doc) stores the document and returns the assigned _id
- get(id) retrieves the document by _id, returning null if not found
- delete(id) removes the document and returns success/failure
- Store documents in a simple file or hash map keyed by _id

## Test Cases

### 1. Index and retrieve a document

doc_index_ok should return a valid _id and result "created".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"doc":{"title":"DS","author":"MK","year":2017}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Get returns indexed document

doc_get_ok should return the same document in _source.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"doc":{"k":"v"}}}
{"src":"c1","dest":"n1","body":{"type":"doc_get","msg_id":3,"_id":"LAST_ID"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Document API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html): Elasticsearch documentation on the Document API

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
