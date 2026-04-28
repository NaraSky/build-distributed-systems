# Implement Anti-Entropy with Digest Comparison

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-4-anti-entropy>

Track: 3. The Gossiper
Task order: 9
Short title: Anti-Entropy
Difficulty: advanced
Subtrack: Gossip Protocol

## Problem

Full state sync wastes bandwidth when nodes are mostly in sync. **Anti-entropy** optimizes this: first exchange compact digests. Only transfer full state if digests differ.

Implement digest-based anti-entropy:

1. `digest` handler returns a hash of the current message set
2. `digest_sync` handler compares digests and only transfers if different
3. Track bandwidth savings

```json
Request:  {"type": "digest", "msg_id": 1}
Response: {"type": "digest_ok", "in_reply_to": 1, "digest": "abc123", "count": 5}
```

```json
Request:  {"type": "digest_sync", "msg_id": 2, "remote_digest": "abc123", "remote_messages": null}
Response: {"type": "digest_sync_ok", "in_reply_to": 2, "match": true, "transferred": 0}
```

If digests differ, the remote sends its messages:
```json
Request:  {"type": "digest_sync", "msg_id": 3, "remote_digest": "xyz789", "remote_messages": [1,2,3]}
Response: {"type": "digest_sync_ok", "in_reply_to": 3, "match": false, "transferred": 2, "local_messages": [1,2,3,4,5]}
```

## Concepts

- anti-entropy
- digest
- set reconciliation
- bandwidth optimization

## Hints

- A digest is a compact summary of your state (e.g., sorted hash of all message IDs)
- Compare digests first; only transfer full state if they differ
- This saves bandwidth when nodes are mostly in sync
- Use a simple hash of sorted message IDs as the digest
- Track bytes saved by using digests vs full sync

## Test Cases

### 1. Digest of empty set

digest_ok should have count=0 and a non-empty digest string.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"digest","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Digest sync with matching digest

digest_ok should have count=1. The digest value can be used for subsequent digest_sync.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"digest","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Merkle Trees for Anti-Entropy](https://en.wikipedia.org/wiki/Merkle_tree): How Merkle trees enable efficient set reconciliation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
