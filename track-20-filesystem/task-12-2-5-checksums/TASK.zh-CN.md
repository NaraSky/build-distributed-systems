# 实现数据块校验和以保障数据完整性

英文标题：Implement Chunk Checksums for Data Integrity
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-5-checksums>

课程：20. 文件系统：容错与再平衡
任务序号：10
短标题：Chunk Checksums
难度：进阶
子主题：Fault Tolerance and Rebalancing

## 中文导读

这道题要求你实现数据块的校验和（Checksum）机制。磁盘有时会"悄悄"损坏数据而不报错，这种静默损坏（Silent Corruption）非常危险。校验和就像数据的"指纹"：每次读取时重新计算并与存储的指纹比对，如果不一致就说明数据被损坏了，需要从其他副本读取。

## 题目说明

磁盘可能在没有任何错误信号的情况下悄悄损坏数据。数据块校验和可以在将损坏的数据返回给用户之前检测到这种问题。

校验和设计：
1. 每个 64MB 的数据块被划分为 64KB 的小块（每个数据块有 1024 个小块）
2. 每个小块有一个 CRC32 校验和（4 字节）。总校验和开销：每个数据块 4KB（仅占 0.006%）
3. 每次读取时，重新计算小块的校验和并与存储的值进行比对
4. 如果匹配：返回数据。如果不匹配：该小块已损坏。

损坏处理流程：
1. 向主节点报告损坏的数据块
2. 从另一个副本读取数据
3. 主节点调度从健康副本进行重新复制
4. 丢弃已损坏的副本

```json
Request:  {"type": "chunk_read_verified", "msg_id": 1, "chunk_handle": "ch_001", "block": 42}
Response: {"type": "chunk_read_verified_ok", "in_reply_to": 1, "data": "...", "checksum_valid": true, "stored_checksum": "abc123", "computed_checksum": "abc123"}

Request:  {"type": "chunk_read_verified", "msg_id": 2, "chunk_handle": "ch_002", "block": 10}
Response: {"type": "chunk_read_verified_ok", "in_reply_to": 2, "checksum_valid": false, "corruption_reported": true, "fallback_server": "cs3"}
```

## 涉及概念

- `checksum`
- `data integrity`
- `corruption detection`
- `per-block checksum`
- `silent corruption`

## 实现提示

- 每个数据块按 64KB 为单位存储一个 CRC32 校验和
- 每次读取时，重新计算校验和并与存储值比对，以检测静默损坏
- 如果发现校验和不匹配，改从另一个副本读取
- 将损坏的数据块报告给主节点，以便主节点调度重新复制
- 磁盘损坏虽然少见但确实存在，谷歌的统计数据显示约 0.01% 的读取会遇到损坏

## 测试用例

### 1. 带校验的读取，校验和匹配

chunk_read_verified_ok 应当显示 checksum_valid: true。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_read_verified","msg_id":2,"chunk_handle":"ch_001","block":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 损坏的数据块触发回退读取

如果 checksum_valid 为 false，那么 corruption_reported 应当为 true，并且 fallback_server 应当有值。

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

- [GFS Data Integrity](https://research.google/pubs/pub51/)：GFS 论文中关于校验和和数据完整性验证的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
