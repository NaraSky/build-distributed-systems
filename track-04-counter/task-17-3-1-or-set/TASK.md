# Implement an OR-Set (Observed-Remove Set)

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-1-or-set>

Track: 4. The Counter
Task order: 11
Short title: OR-Set
Difficulty: advanced
Subtrack: More CRDTs

## Problem

The OR-Set (Observed-Remove Set) solves the concurrent add/remove problem. Each element is tagged with a unique identifier, and remove only removes tags that have been observed.

**Problem with naive sets**: if node A adds "x" and node B concurrently removes "x", what happens? With a naive set, the result depends on message ordering — non-deterministic.

**OR-Set solution**:
- `add("x")`: store `("x", tag_1)` where tag_1 is a unique UUID
- `remove("x")`: remove ALL currently visible pairs for "x": `{("x", tag_1)}`
- If node A does `add("x")` concurrently with node B doing `remove("x")`: node A's add creates tag_2, which node B has never seen. After merge, `("x", tag_2)` survives. **Add wins.**

```json
Request:  {"type": "or_set_add", "msg_id": 1, "element": "apple"}
Response: {"type": "or_set_add_ok", "in_reply_to": 1, "tag": "uuid-001"}

Request:  {"type": "or_set_remove", "msg_id": 2, "element": "apple"}
Response: {"type": "or_set_remove_ok", "in_reply_to": 2, "tags_removed": ["uuid-001"]}

Request:  {"type": "or_set_read", "msg_id": 3}
Response: {"type": "or_set_read_ok", "in_reply_to": 3, "elements": ["banana", "cherry"]}
```

## Concepts

- OR-Set
- observed-remove
- unique tags
- add-wins semantics
- concurrent remove

## Hints

- Each element is stored with a unique tag (UUID) when added
- add(e) creates a new entry: (element, unique_tag)
- remove(e) removes all currently observed (element, tag) pairs for that element
- Concurrent add + remove: the new add has a tag not yet observed by the remove, so it survives
- Merge: union of all (element, tag) pairs from both replicas

## Test Cases

### 1. Add and read element

or_set_read_ok elements should include "apple".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"or_set_add","msg_id":2,"element":"apple"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Remove deletes element

or_set_read_ok elements should NOT include "banana" after removal.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"or_set_add","msg_id":2,"element":"banana"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_remove","msg_id":3,"element":"banana"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [OR-Set CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#OR-Set): Wikipedia article on OR-Set (Observed-Remove Set) CRDT

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
