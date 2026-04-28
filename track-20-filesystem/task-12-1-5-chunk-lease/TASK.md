# Implement Chunk Leases for Primary Assignment

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-5-chunk-lease>

Track: 20. The Filesystem
Task order: 5
Short title: Chunk Lease
Difficulty: advanced
Subtrack: Distributed File Storage

## Problem

A chunk lease grants one chunk server the exclusive right to define the mutation order for a chunk. This avoids per-operation consensus while maintaining consistency.

Lease lifecycle:
1. **Grant**: master assigns a 60-second lease to one chunk server (the primary)
2. **Use**: the primary defines the serial order for all mutations on that chunk
3. **Renew**: primary sends heartbeats to master; master extends the lease
4. **Expire**: if the primary fails to renew within 60s, the lease expires
5. **Re-grant**: master waits for the old lease to expire, then grants to another server

Safety guarantee: at most ONE primary exists for each chunk at any time. If the master loses contact with the primary, it simply waits for the lease to expire before granting to a new server.

```json
Request:  {"type": "lease_grant", "msg_id": 1, "chunk_handle": "ch_001", "server": "cs1"}
Response: {"type": "lease_grant_ok", "in_reply_to": 1, "chunk_handle": "ch_001", "primary": "cs1", "expires_in_ms": 60000}

Request:  {"type": "lease_renew", "msg_id": 2, "chunk_handle": "ch_001", "server": "cs1"}
Response: {"type": "lease_renew_ok", "in_reply_to": 2, "new_expires_in_ms": 60000}

Request:  {"type": "lease_check", "msg_id": 3, "chunk_handle": "ch_001"}
Response: {"type": "lease_check_ok", "in_reply_to": 3, "primary": "cs1", "remaining_ms": 45000, "expired": false}
```

## Concepts

- lease
- primary election
- lease renewal
- lease expiry
- consistency window

## Hints

- A lease grants one chunk server the "primary" role for 60 seconds
- The primary is the only server that can define the mutation order for a chunk
- The primary must renew the lease before it expires (by heartbeating the master)
- If the lease expires, the master can grant it to another server — preventing split-brain
- Leases avoid the cost of per-operation consensus while maintaining consistency

## Test Cases

### 1. Grant lease to chunk server

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_grant","msg_id":2,"chunk_handle":"ch_001","server":"n2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lease_grant_ok", "in_reply_to": 2, "chunk_handle": "ch_001", "primary": "n2", "msg_id": 1}}
```

### 2. Renew lease before expiry

lease_renew_ok should show new_expires_in_ms: 60000 (lease extended).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_grant","msg_id":2,"chunk_handle":"ch_002","server":"n2"}}
{"src":"c1","dest":"n1","body":{"type":"lease_renew","msg_id":3,"chunk_handle":"ch_002","server":"n2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Leases in Distributed Systems](https://dl.acm.org/doi/10.1145/74851.74870): Classic paper on leases as a fault-tolerant mechanism for distributed caches

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
