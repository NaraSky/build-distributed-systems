# 实现追踪分析与洞察

英文标题：Implement Trace Analysis and Insights
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-4-trace-analysis>

课程：25. 追踪器：可观测性
任务序号：4
短标题：Trace Analysis
难度：高级
子主题：Distributed Tracing

## 中文导读

这道题要求你对追踪数据进行分析，从中提炼出有价值的洞察。原始的追踪记录只告诉你"发生了什么"，而追踪分析能告诉你"为什么慢"以及"错误集中在哪里"。通过聚合大量追踪数据，你可以发现性能瓶颈、错误热点和延迟异常，这对排查线上问题至关重要。

## 题目说明

原始追踪数据告诉你发生了什么，而追踪分析则告诉你为什么慢、错误集中在哪里。通过对大量追踪数据进行聚合分析，你可以发现性能瓶颈、错误热点、服务依赖关系和延迟异常值。

请实现一个节点来分析追踪数据并生成洞察报告：

```json
// 识别瓶颈（数据库占据了 94% 的追踪耗时）
{ "type": "analyze_traces", "msg_id": 1,
  "traces": [{"trace_id":"t1","duration_ms":5000,
               "spans":[{"service":"web","duration":100},
                         {"service":"api","duration":200},
                         {"service":"db","duration":4700}]}] }
-> { "type": "insights", "in_reply_to": 1,
    "bottlenecks": ["db"], "critical_path": "web->api->db",
    "optimization_suggestion": "Add caching for database queries" }

// 按服务统计错误率
{ "type": "analyze_errors", "msg_id": 2,
  "traces": [{"trace_id":"t1","has_error":true,"service":"payment-service"},
              {"trace_id":"t2","has_error":false},
              {"trace_id":"t3","has_error":true,"service":"payment-service"}] }
-> { "type": "error_analysis", "in_reply_to": 2,
    "error_rate_by_service": {"payment-service": "66.7%"},
    "total_errors": 2 }
```

## 概念说明

**瓶颈检测**就像在流水线上找最慢的那个工位——如果数据库查询占了整个请求 94% 的时间，那它就是瓶颈。**关键路径**则是从请求入口到最终响应之间耗时最长的那条调用链。找到瓶颈和关键路径后，你就知道该把优化精力放在哪里了。

## 涉及概念

- `bottleneck detection`
- `critical path`
- `error rate`
- `service map`
- `anomaly detection`

## 实现提示

- 瓶颈：占总追踪耗时比例最大的那个跨度
- 关键路径：从根跨度到叶子跨度中，总耗时最长的那条调用链
- 每个服务的错误率 = 该服务的错误追踪数 / 该服务的总追踪数
- 服务拓扑图的边：父跨度所在服务 -> 子跨度所在服务
- 异常检测：追踪耗时 > N 倍的基准 P50（例如 100 倍为高严重度）

## 测试用例

### 1. 性能分析

数据库占据了追踪耗时的 94%，应当被识别为瓶颈。

输入：

```json
{"src":"analyzer","dest":"insights","body":{"type":"analyze_traces","msg_id":1,"time_range":"1h","traces":[{"trace_id":"t1","duration_ms":5000,"spans":[{"service":"web","duration":100},{"service":"api","duration":200},{"service":"db","duration":4700}]}]}}
```

期望输出：

```text
{"type": "insights", "in_reply_to": 1, "bottlenecks": ["db"], "critical_path": "web->api->db", "optimization_suggestion": "Add caching for database queries"}
```

### 2. 错误率分析

payment-service 在 3 条追踪中有 2 条出错，错误率为 66.7%。

输入：

```json
{"src":"analyzer","dest":"insights","body":{"type":"analyze_errors","msg_id":1,"traces":[{"trace_id":"t1","has_error":true,"service":"payment-service"},{"trace_id":"t2","has_error":false},{"trace_id":"t3","has_error":true,"service":"payment-service"}]}}
```

期望输出：

```text
{"type": "error_analysis", "in_reply_to": 1, "error_rate_by_service": {"payment-service": "66.7%"}, "total_errors": 2}
```

## 参考资料

- [Distributed Tracing with Jaeger](https://www.jaegertracing.io/docs/latest/)：Jaeger 关于追踪分析和根因排查的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
