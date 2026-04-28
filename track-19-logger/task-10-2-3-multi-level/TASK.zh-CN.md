# 实现 a Multi-Level LSM Tree

英文标题：Implement a Multi-Level LSM Tree
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-3-multi-level>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：8
短标题：Multi-Level LSM
难度：advanced
子主题：LSM Tree (日志-Structured Merge Tree)

## 中文导读

本题要求你完成 `实现 a Multi-Level LSM Tree`。

重点关注：`multi-level LSM`、`L0`、`L1`、`sorted runs`、`level policy`。

建议先按提示逐步实现：L0 contains unsorted SSTables (recent flushes). Reads must check ALL L0 files.。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A single flat list of SSTables becomes unmanageable as data grows. The multi-level LSM tree organizes SSTables into levels (L0, L1, L2, ...)，包含carefully maintained invariants.

Level structure:
- **L0 (special)**: receives direct flushes from MemTable. SSTables may have overlapping key ranges. Reads must check ALL L0 files.
- **L1, L2, ... (sorted levels)**: SSTables within the same level have non-overlapping key ranges. A read only needs to check at most ONE SSTable per level.
- **Size ratio**: each level is ~10x larger than the previous. L0: 40MB, L1: 400MB, L2: 4GB, L3: 40GB.

Read path (multi-level):
1. Check MemTable (newest data)
2. Check L0 (all files, newest first)
3. Check L1 (binary search by key range, at most 1 file)
4. Check L2, L3, ... until found or exhausted

```JSON
请求:  {"type": "lsm_level_info", "msg_id": 1}
响应: {"type": "lsm_level_info_ok", "in_reply_to": 1, "levels": [
    {"level": 0, "sstables": 4, "total_bytes": 16777216, "sorted": false, "max_bytes": 41943040},
    {"level": 1, "sstables": 5, "total_bytes": 52428800, "sorted": true, "max_bytes": 419430400},
    {"level": 2, "sstables": 10, "total_bytes": 524288000, "sorted": true, "max_bytes": 4194304000}
]}

请求:  {"type": "lsm_read", "msg_id": 2, "key": "user:42"}
响应: {"type": "lsm_read_ok", "in_reply_to": 2, "value": "Alice", "found_at": "L1", "levels_checked": 2}
```

## 涉及概念

- `multi-level LSM`
- `L0`
- `L1`
- `sorted runs`
- `level policy`
- `size ratio`

## 实现提示

- L0 contains unsorted SSTables (recent flushes). Reads must check ALL L0 files.
- L1+ levels are sorted by key range，包含NO overlapping SSTables within a level
- Each level is approximately 10x larger than the previous (size ratio = 10)
- Reads check: MemTable -> L0 (all files) -> L1 -> L2 -> ... until the key is found
- The level selection policy chooses which level to compact based on size limits

## 测试用例

### 1. Level info shows multi-level structure

lsm_level_info_ok should show multiple levels. L0 should have sorted: false, L1+ should have sorted: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_level_info","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read searches levels in order

lsm_read_ok should include found_at level和levels_checked count.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_read","msg_id":2,"key":"user:42"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [LevelDB Implementation Notes](https://github.com/google/leveldb/blob/main/doc/impl.md)：Google LevelDB implementation details explaining multi-level LSM structure

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
