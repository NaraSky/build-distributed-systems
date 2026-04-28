# 实现分布式追踪收集器

英文标题：Implement Distributed Trace Collector
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-3-trace-collector>

课程：25. 追踪器：可观测性
任务序号：3
短标题：Trace Collector
难度：进阶
子主题：Distributed Tracing

## 中文导读

这道题要求你实现一个追踪收集器（Trace Collector），它从多个服务接收跨度数据，按追踪标识分组并组装成完整的追踪记录。收集器还需要支持采样来减少存储量，并妥善处理迟到的跨度。这是构建可观测性基础设施的核心组件。

## 题目说明

追踪收集器（Trace Collector）从多个服务接收跨度，按追踪标识（Trace ID）进行分组，然后将它们组装并存储为完整的追踪记录。它还需要通过采样机制来减少存储开销，并能妥善处理在追踪已完成后才到达的迟到跨度。

请实现一个节点来管理跨度的收集和追踪的组装：

```json
// 来自两个服务的跨度被组装成一条追踪记录
{ "type": "span", "trace_id": "t1", "span_id": "s1", "service": "A" }
{ "type": "span", "trace_id": "t1", "span_id": "s2", "service": "B",
  "parent_span_id": "s1" }
-> { "type": "trace_complete", "trace_id": "t1", "span_count": 2 }

// 1% 采样率：大部分追踪会被拒绝
{ "type": "span", "trace_id": "t2", "service": "fast" }
(sampling_rate: 0.01)
-> { "type": "span_accepted",
    "sampled": false, "reason": "Trace not sampled (1% rate)" }

// 按服务查询追踪记录
{ "type": "query_traces", "msg_id": 1,
  "service": "service-a", "time_range": "1h" }
-> { "type": "query_results", "in_reply_to": 1,
    "traces": 125, "avg_duration_ms": 45 }
```

对于已完成追踪的迟到跨度，应当返回 `"action": "update_trace"` 而不是丢弃它们。

## 概念说明

**追踪收集器**就像一个快递分拣中心。各个服务产生的跨度数据就像包裹，收集器根据追踪标识把属于同一个请求的包裹归到一起。**采样**机制则像是抽检——不需要检查每一个包裹，只抽取一定比例来分析，既能发现问题又不会占用太多资源。

## 涉及概念

- `trace collector`
- `span aggregation`
- `trace sampling`
- `late spans`
- `trace queries`

## 实现提示

- 按 trace_id 对跨度进行分组；当一条追踪收齐所有跨度时，发送 trace_complete
- 采样决策：通过 `hash(trace_id) % 100 < (sampling_rate * 100)` 来对同一条追踪做一致性判断
- query_traces 按服务过滤，返回跨度数量和平均耗时
- 对于已完成追踪的迟到跨度，应当更新该追踪而非丢弃
- 每收到一个属于同一 trace_id 的新跨度，span_count 就加一

## 测试用例

### 1. 将跨度聚合为追踪记录

具有相同 trace_id 的跨度应当被分为一组，并标记追踪完成。

输入：

```json
{"src":"service_a","dest":"collector","body":{"type":"span","trace_id":"t1","span_id":"s1","service":"A"}}
{"src":"service_b","dest":"collector","body":{"type":"span","trace_id":"t1","span_id":"s2","service":"B","parent_span_id":"s1"}}
```

期望输出：

```text
{"type": "trace_complete", "trace_id": "t1", "span_count": 2}
```

### 2. 追踪采样

在 1% 的采样率下，该追踪应当不被采样。

输入：

```json
{"src":"service","dest":"collector","body":{"type":"span","trace_id":"t2","span_id":"s3","service":"fast"},"sampling_rate":0.01}
```

期望输出：

```text
{"type": "span_accepted", "sampled": false, "reason": "Trace not sampled (1% rate)"}
```

## 参考资料

- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)：介绍 OpenTelemetry 收集器如何接收、处理和导出遥测数据

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
