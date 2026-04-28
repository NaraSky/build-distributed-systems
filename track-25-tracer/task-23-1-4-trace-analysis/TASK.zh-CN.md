# 实现 Trace Analysis和Insights

英文标题：Implement Trace Analysis和Insights
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-4-trace-analysis>

课程：25. 追踪器：可观测性
任务序号：4
短标题：Trace Analysis
难度：advanced
子主题：Distributed Tracing

## 中文导读

本题要求你完成 `实现 Trace Analysis和Insights`。

重点关注：`bottleneck detection`、`critical path`、`error rate`、`service map`、`anomaly detection`。

建议先按提示逐步实现：Bottleneck: the span，包含the largest share of total trace duration。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Raw traces tell you what happened. Trace analysis tells you why it was slow和where errors are concentrated. By aggregating many traces, you surface bottlenecks, error hot-spots, service dependencies,和latency outliers.

Implement a 节点 that analyses trace data和surfaces insights:

```JSON
// Identify bottleneck (db takes 94% of trace time)
{ "type": "analyze_traces", "msg_id": 1,
  "traces": [{"trace_id":"t1","duration_ms":5000,
               "spans":[{"service":"web","duration":100},
                         {"service":"api","duration":200},
                         {"service":"db","duration":4700}]}] }
-> { "type": "insights", "in_reply_to": 1,
    "bottlenecks": ["db"], "critical_path": "web->api->db",
    "optimization_suggestion": "Add caching用于database queries" }

// Error rate per service
{ "type": "analyze_errors", "msg_id": 2,
  "traces": [{"trace_id":"t1","has_error":true,"service":"payment-service"},
              {"trace_id":"t2","has_error":false},
              {"trace_id":"t3","has_error":true,"service":"payment-service"}] }
-> { "type": "error_analysis", "in_reply_to": 2,
    "error_rate_by_service": {"payment-service": "66.7%"},
    "total_errors": 2 }
```

## 涉及概念

- `bottleneck detection`
- `critical path`
- `error rate`
- `service map`
- `anomaly detection`

## 实现提示

- Bottleneck: the span，包含the largest share of total trace duration
- Critical path: the chain of spans from root to leaf，包含the maximum total duration
- Error rate per service = error traces用于that service / total traces用于that service
- Service map edges: parent span service -> child span service
- Anomaly: trace duration > N * baseline p50 (e.g. 100x = high severity)

## 测试用例

### 1. Performance analysis

db takes 94% of trace duration和should be identified as bottleneck.

输入：

```json
{"src":"analyzer","dest":"insights","body":{"type":"analyze_traces","msg_id":1,"time_range":"1h","traces":[{"trace_id":"t1","duration_ms":5000,"spans":[{"service":"web","duration":100},{"service":"api","duration":200},{"service":"db","duration":4700}]}]}}
```

期望输出：

```text
{"type": "insights", "in_reply_to": 1, "bottlenecks": ["db"], "critical_path": "web->api->db", "optimization_suggestion": "Add caching用于database queries"}
```

### 2. Error rate analysis

payment-service is in 2/3 error traces = 66.7% error rate.

输入：

```json
{"src":"analyzer","dest":"insights","body":{"type":"analyze_errors","msg_id":1,"traces":[{"trace_id":"t1","has_error":true,"service":"payment-service"},{"trace_id":"t2","has_error":false},{"trace_id":"t3","has_error":true,"service":"payment-service"}]}}
```

期望输出：

```text
{"type": "error_analysis", "in_reply_to": 1, "error_rate_by_service": {"payment-service": "66.7%"}, "total_errors": 2}
```

## 参考资料

- [Distributed Tracing，包含Jaeger](https://www.jaegertracing.io/docs/latest/)：Jaeger docs on trace analysis和root cause investigation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
