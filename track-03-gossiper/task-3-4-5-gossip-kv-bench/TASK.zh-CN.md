# 八卦键值存储的性能基准测试

英文标题：Benchmark Gossip KV Store Performance
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-5-gossip-kv-bench>

课程：3. 传播者：Gossip 信息传播
任务序号：20
短标题：八卦键值存储基准测试
难度：高级
子主题：Epidemic Algorithms and CRDT Gossip

## 中文导读

这道题让你为之前实现的八卦键值存储编写基准测试，量化它的实际表现。你需要关注三个核心指标：所有副本达成一致需要多久（收敛时间）、每次写入产生多少八卦消息（消息开销）、以及读取到过期数据的频率（一致性违例）。通过这些数据，你可以直观地了解八卦传播协议的性能特征。

## 题目说明

对你的八卦键值存储进行基准测试，衡量其实际性能表现：

1. **收敛时间**：所有副本达到相同值需要多长时间？
2. **消息开销**：每次写入操作会产生多少条八卦消息？
3. **一致性违例**：读操作返回过期数据的频率有多高？

实现一个带计时功能的 `bench_write` 接口：
```json
请求:  {"type": "bench_write", "msg_id": 1, "key": "x", "value": "v1"}
响应: {"type": "bench_write_ok", "in_reply_to": 1, "write_id": 1}
```

以及一个 `bench_report` 报告接口：
```json
请求:  {"type": "bench_report", "msg_id": 2}
响应: {"type": "bench_report_ok", "in_reply_to": 2,
           "total_writes": 10, "total_gossip_msgs": 45,
           "msgs_per_write": 4.5, "keys_stored": 5}
```

## 涉及概念

- `benchmarking`
- `convergence time`
- `message overhead`
- `consistency`

## 实现提示

- 记录八卦同步过程中交换的消息总数
- 测量从写入到完全收敛（所有副本一致）所需的时间
- 统计一致性违例次数：即读操作返回过期数据的次数
- 对比正常情况和网络分区情况下的各项指标
- 通过 `bench_stats` 接口暴露这些指标

## 测试用例

### 1. 基准写入返回写入编号

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_write","msg_id":2,"key":"x","value":"v1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bench_write_ok", "write_id": 1, "in_reply_to": 2, "msg_id": 1}}
```

### 2. 零写入时的基准报告

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_report","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bench_report_ok", "total_writes": 0, "total_gossip_msgs": 0, "msgs_per_write": 0, "keys_stored": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Maelstrom Broadcast Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#broadcast)：Maelstrom 广播工作负载的规范文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
