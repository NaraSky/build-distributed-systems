# Implement Dotted Version Vectors

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-4-dotted-version-vectors>

Track: 16. The Timekeeper
Task order: 14
Short title: Dotted Version Vectors
Difficulty: advanced
Subtrack: Vector Clocks

## Problem

Standard vector clocks have an O(N) storage cost that grows with every node that ever participated. Dotted version vectors (DVVs), used in Riak, solve this by separating the **causal context** from the **event dot**.

A DVV has two parts:
- **dot**: `(node_id, counter)` — the single event this value represents
- **version_vector**: the causal context (everything that happened before the dot)

Implement a DVV-based versioning system:

```json
Request:  {"type": "dvv_update", "msg_id": 1, "key": "x", "value": "hello", "context": {}}
Response: {"type": "dvv_update_ok", "in_reply_to": 1, "dot": ["n1", 1], "version_vector": {}}

Request:  {"type": "dvv_update", "msg_id": 2, "key": "x", "value": "world", "context": {"n1": 1}}
Response: {"type": "dvv_update_ok", "in_reply_to": 2, "dot": ["n1", 2], "version_vector": {"n1": 1}}

Request:  {"type": "dvv_get", "msg_id": 3, "key": "x"}
Response: {"type": "dvv_get_ok", "in_reply_to": 3, "values": [{"value": "world", "dot": ["n1", 2]}], "context": {"n1": 2}}
```

## Concepts

- dotted version vectors
- space optimization
- version vectors
- Riak

## Hints

- Standard vector clocks grow linearly with the number of nodes that ever participated
- Dotted version vectors separate the causal context (version vector) from the event dot
- A dot is a (node_id, counter) pair representing a single event
- The version vector represents everything that happened before the dot
- This allows pruning of old entries while preserving correctness

## Test Cases

### 1. First write creates a dot

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":2,"key":"x","value":"hello","context":{}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dvv_update_ok", "in_reply_to": 2, "dot": ["n1", 1], "version_vector": {}, "msg_id": 1}}
```

### 2. Sequential update with context supersedes old value

dvv_get_ok should return only value v2 with dot [n1, 2] since v1 was superseded by context.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":2,"key":"x","value":"v1","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":3,"key":"x","value":"v2","context":{"n1":1}}}
{"src":"c1","dest":"n1","body":{"type":"dvv_get","msg_id":4,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Dotted Version Vectors - Riak Core Concepts](https://riak.com/posts/technical/vector-clocks-revisited-part-2-dotted-version-vectors/): How Riak replaced vector clocks with dotted version vectors for efficiency

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
