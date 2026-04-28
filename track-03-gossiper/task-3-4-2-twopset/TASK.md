# Implement Two-Phase Set (2P-Set)

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-2-twopset>

Track: 3. The Gossiper
Task order: 17
Short title: 2P-Set
Difficulty: advanced
Subtrack: Epidemic Algorithms and CRDT Gossip

## Problem

A **2P-Set** (two-phase set) supports both add and remove by maintaining two G-Sets: the add-set and the remove-set (tombstones). An element is in the set if it is in the add-set but NOT in the remove-set.

```json
Request:  {"type": "add", "msg_id": 1, "element": "x"}
Response: {"type": "add_ok", "in_reply_to": 1}

Request:  {"type": "remove", "msg_id": 2, "element": "x"}
Response: {"type": "remove_ok", "in_reply_to": 2}

Request:  {"type": "read", "msg_id": 3}
Response: {"type": "read_ok", "in_reply_to": 3, "elements": []}

Request:  {"type": "merge", "msg_id": 4, "add_set": ["a","b"], "remove_set": ["b"]}
Response: {"type": "merge_ok", "in_reply_to": 4}
```

## Concepts

- 2P-Set
- CRDT
- tombstone set
- add-remove semantics

## Hints

- A 2P-Set has two internal G-Sets: add-set and remove-set
- To add: insert into add-set. To remove: insert into remove-set
- Value = add-set - remove-set
- Once removed, an element cannot be re-added (tombstone is permanent)
- Merge both G-Sets independently via union

## Test Cases

### 1. Add then read

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"element":"x"}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "elements": ["x"], "in_reply_to": 3, "msg_id": 2}}
```

### 2. Add then remove then read

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"element":"y"}}
{"src":"c1","dest":"n1","body":{"type":"remove","msg_id":3,"element":"y"}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "remove_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "elements": [], "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [CRDTs for Fun and Profit](https://bartoszsypytkowski.com/the-state-of-crdts/): Practical overview of CRDT types and their tradeoffs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
