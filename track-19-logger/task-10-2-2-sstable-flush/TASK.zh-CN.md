# 实现 SSTable Flush，包含Bloom Filter

英文标题：Implement SSTable Flush，包含Bloom Filter
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-2-sstable-flush>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：7
短标题：SSTable Flush
难度：advanced
子主题：LSM Tree (日志-Structured Merge Tree)

## 中文导读

本题要求你完成 `实现 SSTable Flush，包含Bloom Filter`。

重点关注：`SSTable`、`flush`、`Bloom filter`、`immutable file`、`sorted strings`。

建议先按提示逐步实现：When the MemTable exceeds 4MB, sort its entries和flush to an immutable SSTable file on disk。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When the in-memory MemTable exceeds its size threshold, it must be persisted to disk as an SSTable (Sorted String Table). The SSTable is a fundamental building block of LSM trees, used in RocksDB, Cassandra, LevelDB,和HBase.

SSTable properties:
1. **Sorted**: keys are stored in lexicographic order, enabling efficient range scans和merge operations
2. **Immutable**: once written, an SSTable is never modified (append-only philosophy)
3. **Bloom filter**: a probabilistic data structure attached to each SSTable that answers "is this key possibly in this file?"，包含no false negatives
4. **Sparse 索引**: samples every Nth key to enable fast binary search within the file

The flush process:
1. Freeze the current MemTable (stop writes to it, create a new MemTable用于incoming writes)
2. Sort the frozen MemTable entries by key
3. Write them sequentially to a new SSTable file
4. Build the Bloom filter和sparse 索引
5. Write the footer (Bloom filter + 索引)和close the file

```JSON
请求:  {"type": "sstable_flush", "msg_id": 1, "memtable_size_bytes": 4194304}
响应: {"type": "sstable_flush_ok", "in_reply_to": 1, "sstable_file": "L0_001.sst", "entries": 50000, "bloom_filter_bits": 480000, "size_bytes": 4000000}

请求:  {"type": "sstable_lookup", "msg_id": 2, "sstable": "L0_001.sst", "key": "user:42"}
响应: {"type": "sstable_lookup_ok", "in_reply_to": 2, "found": true, "value": "Alice", "bloom_checked": true, "disk_reads": 2}
```

## 涉及概念

- `SSTable`
- `flush`
- `Bloom filter`
- `immutable file`
- `sorted strings`

## 实现提示

- When the MemTable exceeds 4MB, sort its entries和flush to an immutable SSTable file on disk
- SSTable format: sorted key-value pairs followed by an 索引 block和a Bloom filter footer
- The Bloom filter enables O(1) negative lookups: "this key is definitely NOT in this SSTable"
- SSTables are immutable once written — they are never modified, only eventually merged in compaction
- Each SSTable also has a sparse 索引: sample every Nth key用于fast binary search within the file

## 测试用例

### 1. Flush creates SSTable，包含metadata

sstable_flush_ok should include sstable_file name, entries count,和bloom_filter_bits > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"sstable_flush","msg_id":2,"memtable_size_bytes":4194304}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Lookup existing key in SSTable

sstable_lookup_ok should show bloom_checked: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"sstable_flush","msg_id":2,"memtable_size_bytes":1024}}
{"src":"c1","dest":"n1","body":{"type":"sstable_lookup","msg_id":3,"sstable":"L0_001.sst","key":"user:42"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [SSTable和Log Structured Storage](https://www.igvita.com/2012/02/06/sstable-and-log-structured-storage-leveldb/)：How SSTables work in LevelDB和LSM tree 存储 engines

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
