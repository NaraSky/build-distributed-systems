# 实现带布隆过滤器的 SSTable 刷盘

英文标题：Implement SSTable Flush with Bloom Filter
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-2-sstable-flush>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：7
短标题：SSTable Flush
难度：高级
子主题：LSM 树（Log-Structured Merge Tree）

## 中文导读

本题要求你实现将内存表刷写到磁盘生成 SSTable 的过程。SSTable（有序字符串表）是 LSM 树的基础构件，被 RocksDB、Cassandra、LevelDB 等广泛使用。你还需要为每个 SSTable 附加一个布隆过滤器（Bloom Filter），用于快速判断某个键是否可能存在于该文件中。

## 题目说明

当内存中的 MemTable 超过其大小阈值时，必须将其持久化到磁盘，生成一个 SSTable（Sorted String Table，有序字符串表）。SSTable 是 LSM 树的基础构件，被 RocksDB、Cassandra、LevelDB 和 HBase 广泛使用。

SSTable 的特性：
1. **有序**：键按字典序存储，便于高效的范围扫描和归并操作
2. **不可变**：一旦写入，SSTable 就不会再被修改（遵循仅追加的理念）
3. **布隆过滤器（Bloom Filter）**：一种概率型数据结构，附加在每个 SSTable 上，用于回答"这个键是否可能在这个文件中？"，且不会产生假阴性
4. **稀疏索引**：每隔 N 个键采样一次，以便在文件中进行快速的二分查找

刷盘流程如下：
1. 冻结当前 MemTable（停止向其写入，创建一个新的 MemTable 接收新写入）
2. 将冻结的 MemTable 中的条目按键排序
3. 按顺序写入一个新的 SSTable 文件
4. 构建布隆过滤器和稀疏索引
5. 将尾部信息（布隆过滤器 + 索引）写入文件并关闭

```json
Request:  {"type": "sstable_flush", "msg_id": 1, "memtable_size_bytes": 4194304}
Response: {"type": "sstable_flush_ok", "in_reply_to": 1, "sstable_file": "L0_001.sst", "entries": 50000, "bloom_filter_bits": 480000, "size_bytes": 4000000}

Request:  {"type": "sstable_lookup", "msg_id": 2, "sstable": "L0_001.sst", "key": "user:42"}
Response: {"type": "sstable_lookup_ok", "in_reply_to": 2, "found": true, "value": "Alice", "bloom_checked": true, "disk_reads": 2}
```

## 涉及概念

- `SSTable`
- `flush`
- `Bloom filter`
- `immutable file`
- `sorted strings`

## 实现提示

- 当 MemTable 超过 4MB 时，将其条目排序并刷写到磁盘上一个不可变的 SSTable 文件
- SSTable 文件格式：有序的键值对，后面跟着索引块和布隆过滤器的尾部信息
- 布隆过滤器实现 O(1) 的否定查找："这个键肯定不在这个 SSTable 中"
- SSTable 一旦写入就不可变，永远不会被修改，最终只会在压缩过程中被归并
- 每个 SSTable 还有一个稀疏索引：每隔 N 个键采样一次，用于在文件内进行快速二分查找

## 测试用例

### 1. 刷盘生成带元数据的 SSTable

返回的 sstable_flush_ok 中应包含 sstable_file 文件名、entries 条目数以及 bloom_filter_bits > 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"sstable_flush","msg_id":2,"memtable_size_bytes":4194304}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 在 SSTable 中查找已有的键

返回的 sstable_lookup_ok 中应显示 bloom_checked 为 true。

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

- [SSTable and Log Structured Storage](https://www.igvita.com/2012/02/06/sstable-and-log-structured-storage-leveldb/)：介绍 SSTable 在 LevelDB 和 LSM 树存储引擎中的工作原理

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
