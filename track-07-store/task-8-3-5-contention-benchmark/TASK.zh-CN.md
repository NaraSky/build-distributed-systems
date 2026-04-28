# 热点键场景下 OCC 与 MVCC 的基准测试

英文标题：Benchmark Contended Key Under OCC vs MVCC
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-5-contention-benchmark>

课程：7. 存储：线性一致键值存储
任务序号：15
短标题：Contention Benchmark
难度：高级
子主题：基于 Raft 的事务

## 中文导读

这道题要求你对热点键（Hot Key）场景进行基准测试：100 个客户端同时更新同一个键，对比乐观并发控制和多版本并发控制在中止率和吞吐量上的表现。通过这个极端场景的测试，你能清楚地看到不同并发控制策略在高竞争条件下的实际差异。

## 题目说明

对热点键竞争场景进行基准测试：100 个客户端同时更新同一个键，对比乐观并发控制和多版本并发控制在中止率和吞吐量方面的表现。

```json
Request:  {"type": "contention_benchmark", "msg_id": 1, "clients": 100, "key": "hot_key", "ops_per_client": 10, "strategies": ["occ", "mvcc_snapshot", "serializable"]}
Response: {"type": "contention_benchmark_ok", "in_reply_to": 1, "results": [
    {"strategy": "occ", "total_commits": 1000, "total_aborts": 4500, "abort_rate_pct": 81.8, "avg_retries": 4.5, "throughput_commits_sec": 200},
    {"strategy": "mvcc_snapshot", "total_commits": 1000, "total_aborts": 0, "abort_rate_pct": 0, "avg_retries": 0, "throughput_commits_sec": 5000},
    {"strategy": "serializable", "total_commits": 1000, "total_aborts": 900, "abort_rate_pct": 47.4, "avg_retries": 0.9, "throughput_commits_sec": 800}
]}
```

## 涉及概念

- `contention`
- `abort rate`
- `throughput`
- `OCC vs MVCC`
- `hot key`

## 实现提示

- 100 个客户端同时更新同一个键时，乐观并发控制会产生很高的中止率
- 多版本并发控制加快照隔离允许读操作不被阻塞地继续执行
- 可串行化隔离级别会中止冲突的写操作
- 需要测量中止率、吞吐量（提交数/秒）和平均重试次数
- 热点键场景是乐观并发控制最不利的情况

## 测试用例

### 1. 热点键基准测试

验证 contention_benchmark_ok 结果中，乐观并发控制的 abort_rate_pct 高于多版本并发控制。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"contention_benchmark","msg_id":2,"clients":10,"key":"hot_key","ops_per_client":5,"strategies":["occ","mvcc_snapshot"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Concurrency Control in Databases](https://15445.courses.cs.cmu.edu/fall2023/slides/16-concurrencycontrol.pdf)：CMU 15-445 数据库课程关于并发控制机制的讲义

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
