# 实现基于归并排序的 LSM 压缩

英文标题：Implement LSM Compaction with Merge Sort
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-4-compaction>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：9
短标题：LSM Compaction
难度：高级
子主题：LSM 树（Log-Structured Merge Tree）

## 中文导读

本题要求你实现 LSM 树的压缩机制。压缩是一个后台进程，负责将多个 SSTable 归并排序、去重，然后写入目标层级。没有压缩，SSTable 会不断累积，导致读取性能逐渐下降。理解压缩过程及其带来的写放大问题，是深入掌握 LSM 存储引擎的关键。

## 题目说明

压缩（Compaction）是维持 LSM 树健康运行的后台进程。如果没有压缩，越来越多的 SSTable 会不断累积，每次读取都需要更多的磁盘寻道，导致读性能持续下降。

分层压缩算法的步骤如下：
1. **触发**：当 L0 超过 4 个 SSTable，或者某一层超过其大小限制时
2. **选择**：从源层级中选择键范围与目标层级有重叠的 SSTable
3. **归并**：读取所有选中的 SSTable，按键进行归并排序，去重（保留每个键的最新版本）
4. **写入**：将新的有序、无重叠的 SSTable 写入目标层级
5. **清理**：删除旧的源 SSTable

关键指标是**写放大（Write Amplification）**：用户的一次写入，随着数据在各层级间被压缩，可能会被重复写入 10-30 次。这是 LSM 树的根本开销。RocksDB 的分层压缩的写放大大约为 `10 * (层级数 - 1)`。

```json
Request:  {"type": "lsm_compact", "msg_id": 1, "source_level": 0, "target_level": 1}
Response: {"type": "lsm_compact_ok", "in_reply_to": 1, "sstables_merged": 4, "new_sstables": 2, "keys_deduplicated": 500, "bytes_read": 16000000, "bytes_written": 14000000, "write_amplification": 2.3}

Request:  {"type": "lsm_compact_status", "msg_id": 2}
Response: {"type": "lsm_compact_status_ok", "in_reply_to": 2, "pending_compactions": 0, "total_compactions": 5, "total_bytes_compacted": 100000000}
```

## 涉及概念

- `compaction`
- `merge sort`
- `deduplication`
- `write amplification`
- `space reclamation`

## 实现提示

- 当 L0 中有超过 4 个 SSTable 时，将它们归并到 L1（压缩触发条件）
- 压缩就是归并排序：从两个层级中读取有重叠的 SSTable，按键归并，将新的 SSTable 写入目标层级
- 去重：如果同一个键出现在多个 SSTable 中，只保留最新版本
- 写放大 = 写入磁盘的总字节数 / 新数据的总字节数。LSM 树的写放大较高（10-30 倍）
- 压缩完成后，删除已被归并的旧 SSTable

## 测试用例

### 1. 将 L0 压缩到 L1

返回的 lsm_compact_ok 中应显示 sstables_merged > 0 且 write_amplification > 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_compact","msg_id":2,"source_level":0,"target_level":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 压缩时对键进行去重

keys_deduplicated 应 >= 0。bytes_written 应 <= bytes_read（去重会减少数据量）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_compact","msg_id":2,"source_level":0,"target_level":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [RocksDB Compaction](https://github.com/facebook/rocksdb/wiki/Compaction)：RocksDB 关于分层压缩和通用压缩策略的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
