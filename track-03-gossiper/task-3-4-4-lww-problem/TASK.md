# Demonstrate LWW Data Loss with Version Vectors

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-4-lww-problem>

Track: 3. The Gossiper
Task order: 19
Short title: LWW Problem
Difficulty: advanced
Subtrack: Epidemic Algorithms and CRDT Gossip

## Problem

LWW silently loses data when two clients write concurrently. Your task is to demonstrate this and implement a version-vector alternative that detects conflicts.

Implement two modes: `lww` (last-writer-wins) and `vv` (version-vector):

```json
Request:  {"type": "set_mode", "msg_id": 1, "mode": "vv"}
Response: {"type": "set_mode_ok", "in_reply_to": 1}

Request:  {"type": "vv_write", "msg_id": 2, "key": "x", "value": "a", "context": {}}
Response: {"type": "vv_write_ok", "in_reply_to": 2, "vc": {"c1": 1}}

Request:  {"type": "vv_read", "msg_id": 3, "key": "x"}
Response: {"type": "vv_read_ok", "in_reply_to": 3, "values": [{"value": "a", "vc": {"c1": 1}}], "conflict": false}
```

When concurrent writes happen in vv mode, both values are preserved:
```json
Response: {"type": "vv_read_ok", "values": [{"value": "a", "vc": {"c1": 1}}, {"value": "b", "vc": {"c2": 1}}], "conflict": true}
```

## Concepts

- LWW limitation
- data loss
- version vectors
- conflict detection

## Hints

- LWW silently discards the loser in concurrent writes
- Construct a scenario: client A writes x=1, client B writes x=2 at nearly the same time
- The write with the lower timestamp is lost forever
- Version vectors can detect this conflict instead of silently resolving it
- Return both values as siblings when conflict is detected

## Test Cases

### 1. Set mode to vv

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"set_mode","msg_id":2,"mode":"vv"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "set_mode_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Single vv_write and read, no conflict

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vv_write","msg_id":2,"key":"x","value":"a","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"vv_read","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vv_write_ok", "vc": {"c1": 1}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "vv_read_ok", "values": [{"value": "a", "vc": {"c1": 1}}], "conflict": false, "in_reply_to": 3, "msg_id": 2}}
```

## Resources

- [Amazon Dynamo Paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): Dynamo uses version vectors for conflict detection

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
