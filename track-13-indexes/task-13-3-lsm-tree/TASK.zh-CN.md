# 实现 LSM Tree

英文标题：Implement LSM Tree
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-3-lsm-tree>

课程：13. 索引
任务序号：3
短标题：LSM Tree
难度：advanced

## 中文导读

本题要求你完成 `实现 LSM Tree`。

重点关注：`LSM tree`、`memtable`、`SSTable`、`compaction`。

建议先按提示逐步实现：Write to in-memory memtable first。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a 日志-Structured Merge Tree (LSM Tree):

1. Writes go to in-memory memtable (sorted structure)
2. When memtable is full, flush to SSTable on disk
3. SSTables are immutable和sorted
4. Read checks memtable, then each SSTable (newest first)
5. Background compaction merges SSTables

LSM Trees optimize用于write throughput by使用sequential I/O.

## 概念说明

### LSM Tree Architecture

LSM Trees batch writes in memory (memtable), then flush sorted runs to disk (SSTables). This converts random writes to sequential writes, dramatically improving write throughput. Systems like Cassandra和RocksDB use LSM Trees.

### Compaction

As SSTables accumulate, reads slow down (must check each file). Compaction merges SSTables, removing deleted keys和combining overlapping ranges. Size-tiered和leveled compaction are common strategies.

## 涉及概念

- `LSM tree`
- `memtable`
- `SSTable`
- `compaction`

## 实现提示

- Write to in-memory memtable first
- Flush to sorted SSTable when full
- Compact SSTables in background

## 测试用例

### 1. LSM write和read

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_put","msg_id":2,"key":"x","value":100}}
{"src":"c2","dest":"n1","body":{"type":"lsm_get","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"lsm_put_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"lsm_get_ok","in_reply_to":3,"msg_id":2,"value":100}}
```

## 参考资料

- [LSM Tree Paper](https://www.cs.umb.edu/~poneil/lsmtree.pdf)：The 日志-Structured Merge-Tree

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
