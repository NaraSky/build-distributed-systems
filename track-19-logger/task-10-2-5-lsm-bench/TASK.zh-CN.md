# LSM 树与 B 树性能基准测试

网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-5-lsm-bench>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：10
短标题：LSM 基准测试
难度：进阶
子主题：LSM 树（Log-Structured Merge Tree）

## 中文导读

几乎所有数据库的底层都要面对一个选择题：用 LSM 树还是 B 树来组织数据？这两种数据结构代表了截然不同的设计哲学。LSM 树把随机写入变成顺序写入，写得快但读起来可能要查多个地方；B 树直接在原位修改数据，读得快但写入涉及随机磁盘访问。

这道题让你对两种引擎做基准测试，用实际数据来直观感受它们各自的优势和劣势，理解为什么不同的数据库会做出不同的选择。

## 题目说明

在 LSM 树和 B 树之间做选择，是存储引擎设计中最重要的决策之一。两者代表了截然不同的权衡：

**LSM 树**（代表产品：RocksDB、Cassandra、LevelDB）：
- 写入是顺序操作（先追加到内存表 MemTable，再刷写到磁盘上的有序表 SSTable），因此写入吞吐量非常高
- 读取时可能需要检查多个层级才能找到数据，因此读取延迟相对较高
- 空间放大（Space Amplification）大于 1.0，因为旧版本的数据在压缩（Compaction）完成之前一直存在
- 写放大（Write Amplification）较高，数据在压缩过程中会被反复重写

**B 树**（代表产品：PostgreSQL、MySQL InnoDB、SQLite）：
- 写入是随机磁盘访问（直接在原位更新数据页），因此写入吞吐量较低
- 读取沿着平衡树遍历，只需 O(log N) 次磁盘读取，因此读取延迟较低
- 空间放大接近 1.0，因为是原地更新，不会保留过期版本
- 写放大较低

请对两种引擎进行基准测试，分别测量：写入每秒操作数、读取中位延迟（p50）和空间放大率。

```json
Request:  {"type": "lsm_benchmark", "msg_id": 1, "entries": 100000}
Response: {"type": "lsm_benchmark_ok", "in_reply_to": 1, "lsm": {"write_ops_sec": 200000, "read_p50_us": 50, "read_without_bloom_p50_us": 500, "space_amplification": 1.3}, "btree": {"write_ops_sec": 50000, "read_p50_us": 20, "space_amplification": 1.0}}
```

## 涉及概念

- `write throughput`
- `read latency`
- `space amplification`
- `Bloom filter impact`
- `engine comparison`

## 实现提示

- 测量写入吞吐量：LSM 树擅长顺序插入，因为所有写入都是追加操作
- 分别测量有布隆过滤器（Bloom Filter）和没有布隆过滤器时的读取延迟。布隆过滤器能快速判断某个键是否不在某个 SSTable 中，从而大幅减少不必要的磁盘读取
- 空间放大 = 磁盘上占用的总空间 / 有效数据的总大小。LSM 树的空间放大大于 1.0，因为压缩前会存在重复版本的数据
- 与 B 树进行对比：B 树的读取延迟更低，但写入延迟更高（需要原地更新）
- 简单来说：写多读少选 LSM 树，读多写少选 B 树

## 测试用例

### 1. 完整基准测试对比

返回的 `lsm_benchmark_ok` 中应同时包含 LSM 树和 B 树的结果。LSM 树的 `write_ops_sec` 应更高，B 树的 `read_p50_us` 应更低。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_benchmark","msg_id":2,"entries":1000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 布隆过滤器对读取性能的影响

LSM 树带布隆过滤器时的 `read_p50_us` 应明显小于不带时的 `read_without_bloom_p50_us`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_benchmark","msg_id":2,"entries":5000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Designing Data-Intensive Applications](https://dataintensive.net/)：Martin Kleppmann 所著，第三章深入对比了 LSM 树与 B 树两种存储引擎的设计权衡，是理解存储引擎选型的最佳参考

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
