# 基准测试 Contended Key Under OCC vs MVCC

英文标题：Benchmark Contended Key Under OCC vs MVCC
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-5-contention-benchmark>

课程：7. 存储：线性一致 KV Store
任务序号：15
短标题：Contention 基准测试
难度：advanced
子主题：Transactions on Raft

## 中文导读

本题要求你完成 `基准测试 Contended Key Under OCC vs MVCC`。

重点关注：`contention`、`abort rate`、`throughput`、`OCC vs MVCC`、`hot key`。

建议先按提示逐步实现：With 100 clients all updating the same key, OCC will have high abort rates。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Benchmark a contended-key scenario: 100 clients all updating the same key simultaneously. Compare OCC vs MVCC in terms of abort rate和throughput.

```JSON
请求:  {"type": "contention_benchmark", "msg_id": 1, "clients": 100, "key": "hot_key", "ops_per_client": 10, "strategies": ["occ", "mvcc_snapshot", "serializable"]}
响应: {"type": "contention_benchmark_ok", "in_reply_to": 1, "results": [
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

- With 100 clients all updating the same key, OCC will have high abort rates
- MVCC + snapshot isolation allows readers to proceed without blocking
- Serializable isolation aborts conflicting writes
- Measure abort rate, throughput (commits/sec),和average retries
- The hot key scenario is worst-case用于OCC

## 测试用例

### 1. 基准测试 contended key

contention_benchmark_ok should show OCC，包含higher abort_rate_pct than MVCC.

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

- [Concurrency Control in Databases](https://15445.courses.cs.cmu.edu/fall2023/slides/16-concurrencycontrol.pdf)：CMU 15-445 lecture on concurrency control mechanisms

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
