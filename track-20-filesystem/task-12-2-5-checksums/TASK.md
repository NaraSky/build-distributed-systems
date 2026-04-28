# Implement Chunk Checksums for Data Integrity

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-5-checksums>

Track: 20. The Filesystem
Task order: 10
Short title: Chunk Checksums
Difficulty: intermediate
Subtrack: Fault Tolerance and Rebalancing

## Problem

Disks can silently corrupt data without any error signal. Chunk checksums detect this corruption before it is returned to users.

Checksum design:
1. Each 64MB chunk is divided into 64KB blocks (1024 blocks per chunk)
2. Each block has a CRC32 checksum (4 bytes). Total checksum overhead: 4KB per chunk (0.006%)
3. On every read, recompute the block checksum and compare to the stored value
4. If they match: return the data. If they mismatch: the block is corrupted.

Corruption handling:
1. Report the corrupted chunk to the master
2. Read from another replica
3. Master schedules re-replication from a healthy replica
4. The corrupted replica is discarded

```json
Request:  {"type": "chunk_read_verified", "msg_id": 1, "chunk_handle": "ch_001", "block": 42}
Response: {"type": "chunk_read_verified_ok", "in_reply_to": 1, "data": "...", "checksum_valid": true, "stored_checksum": "abc123", "computed_checksum": "abc123"}

Request:  {"type": "chunk_read_verified", "msg_id": 2, "chunk_handle": "ch_002", "block": 10}
Response: {"type": "chunk_read_verified_ok", "in_reply_to": 2, "checksum_valid": false, "corruption_reported": true, "fallback_server": "cs3"}
```

## Concepts

- checksum
- data integrity
- corruption detection
- per-block checksum
- silent corruption

## Hints

- Each chunk stores a CRC32 checksum per 64KB block
- On every read, recompute the checksum and compare — detect silent corruption
- If a checksum mismatch is found, read from another replica instead
- Report corrupted chunks to the master so it can schedule re-replication
- Disk corruption is rare but real — Google reports ~0.01% of reads hit corruption

## Test Cases

### 1. Verified read with valid checksum

chunk_read_verified_ok should show checksum_valid: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_read_verified","msg_id":2,"chunk_handle":"ch_001","block":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Corrupted block triggers fallback

If checksum_valid is false, corruption_reported should be true and fallback_server should be set.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_read_verified","msg_id":2,"chunk_handle":"ch_002","block":10}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [GFS Data Integrity](https://research.google/pubs/pub51/): GFS paper section on checksums and data integrity verification

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
