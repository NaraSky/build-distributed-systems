# 基准测试节点吞吐量和延迟

英文标题：Benchmark节点Throughput和Latency
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-4-throughput-bench>

课程：1. 信使：消息通信基础
任务序号：14
短标题：吞吐量 Bench
难度：intermediate
子主题：The Protocol Beneath

## 中文导读

本题要求你完成 `基准测试节点吞吐量和延迟`。

重点关注：`benchmarking`、`throughput`、`latency`、`profiling`、`performance`。

建议先按提示逐步实现：Track timestamps用于each 消息 received和each 响应 sent。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

How fast is your 节点? In production systems, you need to measure **throughput** (消息 per second)和**latency** (time to process each 消息). Profiling reveals whether the bottleneck is in parsing, dispatch, or serialization.

Your task is to add benchmarking to your 节点:

1. Track the timestamp of each incoming 消息和each outgoing 响应
2. Compute per-消息 latency (time from receive to send)
3. Compute overall throughput (消息 processed per second)
4. Report statistics via a `bench_stats` 消息 type

```JSON
请求:  {"type": "bench_stats", "msg_id": 1}
响应: {"type": "bench_stats_ok", "in_reply_to": 1, 
           "total_messages": 100, 
           "elapsed_ms": 523,
           "throughput_per_sec": 191.2,
           "avg_latency_us": 45,
           "p99_latency_us": 120}
```

Additionally implement a `bench_echo` type that is identical to echo but records timing:
```JSON
请求:  {"type": "bench_echo", "msg_id": 1, "echo": "perf"}
响应: {"type": "bench_echo_ok", "in_reply_to": 1, "echo": "perf", "latency_us": 42}
```

## 涉及概念

- `benchmarking`
- `throughput`
- `latency`
- `profiling`
- `performance`

## 实现提示

- Track timestamps用于each 消息 received和each 响应 sent
- Throughput = total 消息 / elapsed time
- Latency = time between receiving a 消息和sending the 响应
- Use time.monotonic()用于accurate elapsed time measurements
- Store latency samples to compute percentiles (p50, p99)

## 测试用例

### 1. 初始化和回声 still work

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"bench"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "bench", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Bench 回声 includes latency_us field

The second output line is a bench_echo_ok，包含echo="perf"和a latency_us integer field. Exact latency varies so only structure is validated.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_echo","msg_id":2,"echo":"perf"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Latency Numbers Every Programmer Should Know](https://colin-scott.github.io/personal_website/research/interactive_latency.html)：Interactive visualization of latency at different system levels

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
