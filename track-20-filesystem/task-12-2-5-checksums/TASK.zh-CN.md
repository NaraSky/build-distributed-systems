# 实现 Chunk Checksums用于Data Integrity

英文标题：Implement Chunk Checksums用于Data Integrity
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-5-checksums>

课程：20. 文件系统：分布式文件存储
任务序号：10
短标题：Chunk Checksums
难度：intermediate
子主题：Fault Tolerance和Rebalancing

## 中文导读

本题要求你完成 `实现 Chunk Checksums用于Data Integrity`。

重点关注：`checksum`、`data integrity`、`corruption detection`、`per-block checksum`、`silent corruption`。

建议先按提示逐步实现：Each chunk stores a CRC32 checksum per 64KB block。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Disks can silently corrupt data without any error signal. Chunk checksums detect this corruption before it is returned to users.

Checksum design:
1. Each 64MB chunk is divided into 64KB blocks (1024 blocks per chunk)
2. Each block has a CRC32 checksum (4 bytes). Total checksum overhead: 4KB per chunk (0.006%)
3. On every read, recompute the block checksum和compare to the stored value
4. If they match: return the data. If they mismatch: the block is corrupted.

Corruption handling:
1. Report the corrupted chunk to the master
2. Read from another replica
3. Master schedules re-复制 from a healthy replica
4. The corrupted replica is discarded

```JSON
请求:  {"type": "chunk_read_verified", "msg_id": 1, "chunk_handle": "ch_001", "block": 42}
响应: {"type": "chunk_read_verified_ok", "in_reply_to": 1, "data": "...", "checksum_valid": true, "stored_checksum": "abc123", "computed_checksum": "abc123"}

请求:  {"type": "chunk_read_verified", "msg_id": 2, "chunk_handle": "ch_002", "block": 10}
响应: {"type": "chunk_read_verified_ok", "in_reply_to": 2, "checksum_valid": false, "corruption_reported": true, "fallback_server": "cs3"}
```

## 涉及概念

- `checksum`
- `data integrity`
- `corruption detection`
- `per-block checksum`
- `silent corruption`

## 实现提示

- Each chunk stores a CRC32 checksum per 64KB block
- On every read, recompute the checksum和compare — detect silent corruption
- If a checksum mismatch is found, read from another replica instead
- Report corrupted chunks to the master so it can schedule re-复制
- Disk corruption is rare but real — Google reports ~0.01% of reads hit corruption

## 测试用例

### 1. Verified read，包含valid checksum

chunk_read_verified_ok should show checksum_valid: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_read_verified","msg_id":2,"chunk_handle":"ch_001","block":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Corrupted block triggers fallback

If checksum_valid is false, corruption_reported should be true和fallback_server should be set.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_read_verified","msg_id":2,"chunk_handle":"ch_002","block":10}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [GFS Data Integrity](https://research.google/pubs/pub51/)：GFS paper section on checksums和data integrity verification

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
