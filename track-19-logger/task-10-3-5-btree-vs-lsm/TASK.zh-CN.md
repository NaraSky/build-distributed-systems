# 对比 B 树与 LSM 树的放大指标

英文标题：Compare B-Tree vs LSM Tree with Amplification Metrics
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-5-btree-vs-lsm>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：15
短标题：B-Tree vs LSM
难度：进阶
子主题：B-Tree on Disk

## 中文导读

本题要求你对比 B 树和 LSM 树在不同工作负载下的性能表现，核心评估指标是三个"放大因子"：读放大、写放大和空间放大。理解这些指标能帮助你在实际项目中做出正确的存储引擎选择——这是数据库架构设计中最重要的决策之一。

## 题目说明

在 B 树和 LSM 树之间做选择，是存储引擎设计中最重要的决策之一。它们分别针对读写频谱的两端做了优化。理解以下三个放大因子是关键：

**读放大（Read Amplification）**——每次逻辑读需要多少次磁盘读取：
- B 树：O(log_B(N))，其中 B 是分支因子。通常只需 2-4 次读取。
- LSM 树：需要依次检查内存表、L0 层（所有文件）、L1、L2 等等。布隆过滤器（Bloom Filter）能减少查找次数，但最坏情况下需要检查每一层。

**写放大（Write Amplification）**——每写入 1 字节用户数据，实际写入磁盘多少字节：
- B 树：约 2 倍（读取页面、修改、写回）。如果加上预写日志：约 3 倍。
- LSM 树：10-30 倍。数据先写入内存表，刷到 L0，然后逐层压缩经过 L1、L2、L3 等。

**空间放大（Space Amplification）**——实际磁盘占用与逻辑数据量的比值：
- B 树：约 1.0（原地更新，没有旧版本残留）。分裂可能导致少量碎片。
- LSM 树：1.1-1.5（旧版本在被压缩清除之前一直存在）。

如何选择：
- B 树：PostgreSQL、MySQL（联机事务处理，读写混合负载）
- LSM 树：RocksDB、Cassandra（写入密集型、时间序列、日志类场景）

```json
Request:  {"type": "btree_vs_lsm", "msg_id": 1, "entries": 100000, "workload": {"read_pct": 50, "write_pct": 50}}
Response: {"type": "btree_vs_lsm_ok", "in_reply_to": 1, "btree": {"write_ops_sec": 50000, "read_ops_sec": 200000, "space_amp": 1.0, "write_amp": 3.0, "read_amp": 1.0}, "lsm": {"write_ops_sec": 200000, "read_ops_sec": 80000, "space_amp": 1.3, "write_amp": 10.0, "read_amp": 3.0}}
```

## 涉及概念

- `performance comparison`
- `read amplification`
- `write amplification`
- `space amplification`
- `engine selection`

## 实现提示

- 读放大：每次逻辑读需要多少次磁盘读取。B 树为 O(log N)，LSM 树为 O(层数 * 扇出)
- 写放大：每字节用户数据对应多少字节的磁盘写入。B 树约 2 倍，LSM 树为 10-30 倍
- 空间放大：磁盘占用与逻辑数据量的比值。B 树约 1.0，LSM 树为 1.1-1.5（存在旧版本）
- B 树擅长：读密集型事务处理、点查询、配合缓冲池的范围扫描
- LSM 树擅长：写密集型负载、日志记录、时间序列、类似 Kafka 的追加写入场景

## 测试用例

### 1. 混合负载下对比两种引擎

LSM 树的写入吞吐量（write_ops_sec）应更高，B 树的读取吞吐量（read_ops_sec）应更高且空间放大（space_amp）更低。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_vs_lsm","msg_id":2,"entries":1000,"workload":{"read_pct":50,"write_pct":50}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 读密集型负载有利于 B 树

在读密集型负载下，B 树的读取吞吐量（read_ops_sec）应明显高于 LSM 树。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_vs_lsm","msg_id":2,"entries":1000,"workload":{"read_pct":90,"write_pct":10}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [B-Tree vs LSM Tree Analysis](https://www.usenix.org/system/files/login/articles/login_oct15_05_bender.pdf)：深入分析写放大、读放大和空间放大之间权衡的学术论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
