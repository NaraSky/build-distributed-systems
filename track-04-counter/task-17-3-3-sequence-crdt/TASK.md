# Implement a Sequence CRDT for Collaborative Text Editing

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-3-sequence-crdt>

Track: 4. The Counter
Task order: 13
Short title: Sequence CRDT
Difficulty: advanced
Subtrack: More CRDTs

## Problem

A Sequence CRDT enables collaborative text editing where multiple users can type simultaneously without conflicts. The RGA (Replicated Growable Array) assigns each character a unique, ordered position identifier.

**RGA design**:
- Each character has a unique ID: `(lamport_timestamp, node_id)`
- Characters are ordered by their IDs — the document is the sorted sequence
- Insert between positions P1 and P2: create a new ID between them
- Delete: mark the character as a tombstone (keep the ID for ordering)

**Concurrent inserts**: if two users insert at the same position, the tiebreaker is the node ID. This ensures deterministic ordering across all replicas.

```json
Request:  {"type": "seq_insert", "msg_id": 1, "position": 0, "char": "H"}
Response: {"type": "seq_insert_ok", "in_reply_to": 1, "id": "1-n1"}

Request:  {"type": "seq_read", "msg_id": 2}
Response: {"type": "seq_read_ok", "in_reply_to": 2, "text": "Hello", "length": 5}
```

## Concepts

- sequence CRDT
- RGA
- collaborative editing
- position identifiers
- concurrent inserts

## Hints

- Use RGA (Replicated Growable Array): each character has a unique position ID
- Position IDs are ordered and never change — new characters get IDs between neighbors
- Delete marks a character as a tombstone (never physically removed)
- Concurrent inserts at the same position are ordered by node ID (tiebreaker)
- The final document is the sequence of non-tombstoned characters in position order

## Test Cases

### 1. Insert and read characters

seq_read_ok text should be "Hi".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":2,"position":0,"char":"H"}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":3,"position":1,"char":"i"}}
{"src":"c1","dest":"n1","body":{"type":"seq_read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Delete marks character as tombstone

seq_read_ok text should be "B" (A was deleted).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":2,"position":0,"char":"A"}}
{"src":"c1","dest":"n1","body":{"type":"seq_insert","msg_id":3,"position":1,"char":"B"}}
{"src":"c1","dest":"n1","body":{"type":"seq_delete","msg_id":4,"position":0}}
{"src":"c1","dest":"n1","body":{"type":"seq_read","msg_id":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [RGA: Replicated Growable Array](https://doi.org/10.1016/j.jpdc.2010.12.006): Roh et al. - Replicated abstract data types: Building blocks for collaborative applications

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
