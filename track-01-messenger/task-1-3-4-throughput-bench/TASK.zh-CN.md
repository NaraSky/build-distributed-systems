# 基准测试：测量节点的吞吐量和延迟

英文标题：Benchmark Node Throughput and Latency
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-4-throughput-bench>

课程：1. 信使：消息通信基础
任务序号：14
短标题：吞吐量基准测试
难度：进阶
子主题：协议底层机制

## 中文导读

你写的节点到底有多快？在生产系统中，你需要量化两个关键指标：吞吐量（每秒能处理多少条消息）和延迟（处理每条消息需要多少时间）。这道题要求你给节点添加性能测量功能，并通过消息接口报告统计数据。

性能基准测试是优化系统的起点——不量化就无法优化。了解吞吐量和延迟的概念，对理解分布式系统的容量规划至关重要。

## 题目说明

你的节点处理消息有多快？在生产系统中，需要度量两个核心性能指标：

- **吞吐量（Throughput）**：每秒能处理多少条消息
- **延迟（Latency）**：从收到一条消息到发出响应需要多长时间

通过性能分析，可以定位瓶颈是在 JSON 解析、消息分发还是序列化环节。

你的任务是给节点添加基准测试功能：

1. 记录每条收到消息和发出响应的时间戳
2. 计算单条消息的延迟（从收到到发出的时间差）
3. 计算整体吞吐量（每秒处理的消息数）
4. 通过 `bench_stats` 消息类型报告统计数据

```json
Request:  {"type": "bench_stats", "msg_id": 1}
Response: {"type": "bench_stats_ok", "in_reply_to": 1, 
           "total_messages": 100, 
           "elapsed_ms": 523,
           "throughput_per_sec": 191.2,
           "avg_latency_us": 45,
           "p99_latency_us": 120}
```

还需要实现 `bench_echo` 消息类型，它和普通的 `echo` 功能一样，但会在响应中附带本次处理的延迟：

```json
Request:  {"type": "bench_echo", "msg_id": 1, "echo": "perf"}
Response: {"type": "bench_echo_ok", "in_reply_to": 1, "echo": "perf", "latency_us": 42}
```

## 概念说明

### 吞吐量和延迟的区别

打个比方：吞吐量就像高速公路每小时能通过多少辆车，延迟就像一辆车从入口到出口需要多长时间。一条四车道的高速公路吞吐量很高，但如果路上堵车了，每辆车的延迟也会很大。在分布式系统中，高吞吐量和低延迟往往不能兼得，需要根据业务需求做权衡。

### 百分位延迟

平均延迟有时会掩盖问题。比如 99 条请求都在 1 毫秒内完成，但有 1 条花了 10 秒，平均下来才 101 毫秒——看起来还行。但对那个等了 10 秒的用户来说，体验很糟糕。所以我们还需要关注 **P99 延迟**（99% 的请求在这个时间内完成）、**P50 延迟**（中位数延迟）等百分位指标。

### 为什么需要基准测试

不量化就无法优化。基准测试帮你回答这些问题：节点的瓶颈在哪？JSON 解析占了多少时间？加了新功能后性能下降了多少？这些数据是做架构决策的基础。

## 涉及概念

- `benchmarking`
- `throughput`
- `latency`
- `profiling`
- `performance`

## 实现提示

- 记录每条消息的接收时间戳和每个响应的发送时间戳
- 吞吐量 = 总消息数 / 总耗时
- 延迟 = 收到消息到发出响应之间的时间差
- 使用 `System.nanoTime()` 来获取高精度时间（注意单位是纳秒）
- 保存延迟采样值，用于计算百分位数（P50、P99）

## 测试用例

### 1. 初始化和回声功能正常

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

### 2. bench_echo 响应中包含 latency_us 字段

第二行输出是 `bench_echo_ok`，包含 `echo="perf"` 和一个整数类型的 `latency_us` 字段。由于延迟的具体值会变化，测试只检查响应结构是否正确。

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

- [Latency Numbers Every Programmer Should Know](https://colin-scott.github.io/personal_website/research/interactive_latency.html)：交互式延迟可视化工具，展示不同系统层级的延迟量级

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
