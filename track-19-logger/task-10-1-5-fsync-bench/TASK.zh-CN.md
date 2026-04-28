# WAL 的 fsync 策略基准测试

网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-5-fsync-bench>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：5
短标题：fsync 基准测试
难度：进阶
子主题：提交日志（WAL）

## 中文导读

当你往文件里写数据时，数据并不会立刻落到磁盘上。操作系统为了提高性能，会先把数据放在内存缓冲区里，过一会儿再统一写入磁盘。这意味着如果此时突然断电，缓冲区里的数据就丢了。`fsync` 就是用来解决这个问题的系统调用——它强制把数据从内存刷到磁盘。

这道题让你对比三种不同的刷盘策略，亲身感受"数据安全"和"写入速度"之间的权衡。这是设计任何需要持久化数据的系统时都必须面对的核心问题。

## 题目说明

`fsync` 系统调用的作用是强制操作系统将数据从内核缓冲区刷写到物理磁盘上。如果不调用它，那些看起来已经"写好"的数据可能只是存在于内存中，一旦断电就会丢失。

这背后有一个根本性的权衡：**数据持久性和写入吞吐量不可兼得**。

从最安全到最快，有三种策略可供选择：

1. **每次写入都 fsync**：每写一条数据就调用一次 fsync。好处是每条已确认的数据都已经安全落盘；坏处是写入速度受限于磁盘的每秒操作次数（IOPS）。
2. **批量 fsync**：先把写入操作攒起来，每隔 10 毫秒统一调用一次 fsync。崩溃时最多丢失 10 毫秒内的写入数据，但吞吐量可以提升 10 到 30 倍。
3. **不 fsync**：完全不主动刷盘，让操作系统自行决定何时写入磁盘。崩溃时可能丢失数秒的数据，但吞吐量可以提升 100 倍以上。

请对这三种策略进行基准测试，测量每种策略的每秒操作数，直观感受持久性和吞吐量之间的权衡曲线。

```json
Request:  {"type": "fsync_benchmark", "msg_id": 1, "entries": 10000, "strategies": ["always", "batch_10ms", "none"]}
Response: {"type": "fsync_benchmark_ok", "in_reply_to": 1, "results": [
    {"strategy": "always", "ops_per_sec": 500, "durability": "every_write", "data_loss_window": "0ms"},
    {"strategy": "batch_10ms", "ops_per_sec": 15000, "durability": "every_10ms", "data_loss_window": "10ms"},
    {"strategy": "none", "ops_per_sec": 100000, "durability": "os_dependent", "data_loss_window": "seconds"}
]}
```

## 涉及概念

- `fsync`
- `durability`
- `throughput tradeoff`
- `batch sync`
- `OS buffering`

## 实现提示

- 每次写入都 fsync：每条数据都安全落盘，但机械硬盘每秒大约只能做 500 次 fsync
- 每 10 毫秒批量 fsync：把多次写入攒在一起，一次性刷盘。在安全性和性能之间取得了不错的平衡，最多丢 10 毫秒的数据
- 不 fsync：吞吐量最高，但崩溃时可能丢失数秒的数据
- 固态硬盘的 fsync 性能远好于机械硬盘，每秒可达 10000 次以上
- 生产级系统如 PostgreSQL 提供了 `wal_sync_method` 配置项，让用户根据业务需求选择合适的同步策略

## 测试用例

### 1. 对三种策略进行基准测试

结果应包含 3 条记录，每秒操作数依次递增：always < batch_10ms < none。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"fsync_benchmark","msg_id":2,"entries":100,"strategies":["always","batch_10ms","none"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 单一策略基准测试

结果应包含 1 条记录，strategy 为 "always"，data_loss_window 为 "0ms"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"fsync_benchmark","msg_id":2,"entries":50,"strategies":["always"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [PostgreSQL WAL Reliability](https://www.postgresql.org/docs/current/wal-reliability.html)：PostgreSQL 关于预写日志可靠性、fsync 和数据完整性的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
