# Implement etcd MVCC for Versioned Key-Value Store

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-5-mvcc>

Track: 22. The Watcher
Task order: 15
Short title: etcd MVCC
Difficulty: advanced
Subtrack: Consistency and the ZAB Protocol

## Problem

etcd's MVCC (Multi-Version Concurrency Control) stores every version of every key. This enables historical reads and safe watch catch-up.

**How it works**:
1. Every modification increments a global revision counter
2. `Put("/config", "v1")` stores the value at revision 42
3. `Put("/config", "v2")` stores the value at revision 43
4. `Get("/config")` returns "v2" at revision 43 (latest)
5. `Get("/config", revision=42)` returns "v1" (historical read)

**Compaction**: old revisions are removed to save space. `Compact(revision=40)` deletes all versions before revision 40. Historical reads before revision 40 will fail.

**Watch safety**: a watcher at revision 42 can always catch up, even if it temporarily disconnects, by requesting changes since revision 42.

```json
Request:  {"type": "etcd_put", "msg_id": 1, "key": "/cfg", "value": "v1"}
Response: {"type": "etcd_put_ok", "in_reply_to": 1, "revision": 1}

Request:  {"type": "etcd_get", "msg_id": 2, "key": "/cfg", "revision": 1}
Response: {"type": "etcd_get_ok", "in_reply_to": 2, "key": "/cfg", "value": "v1", "mod_revision": 1}

Request:  {"type": "etcd_compact", "msg_id": 3, "revision": 5}
Response: {"type": "etcd_compact_ok", "in_reply_to": 3, "compacted_to": 5, "versions_removed": 12}
```

## Concepts

- MVCC
- multi-version concurrency
- revision
- compaction
- historical reads

## Hints

- Every key has multiple versions, indexed by a global revision counter
- Put increments the global revision and stores the key at that revision
- Get(key, revision=N) retrieves the value at revision N (historical read)
- Compact(revision=N) removes all versions before N to save space
- MVCC enables safe watches: even if a watch falls behind, it can catch up from a known revision

## Test Cases

### 1. Historical read returns old version

etcd_get_ok at revision 1 should return value "v1".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/k","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":3,"key":"/k","value":"v2"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_get","msg_id":4,"key":"/k","revision":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compact removes old versions

etcd_compact_ok should show compacted_to and versions_removed >= 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_compact","msg_id":2,"revision":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [etcd MVCC](https://etcd.io/docs/v3.5/learning/data_model/): etcd documentation on MVCC data model and revision-based versioning

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
