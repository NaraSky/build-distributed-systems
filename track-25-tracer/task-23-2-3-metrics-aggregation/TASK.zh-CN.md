# 实现 Metrics Aggregation和Rollups

英文标题：Implement Metrics Aggregation和Rollups
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-3-metrics-aggregation>

课程：25. 追踪器：可观测性
任务序号：8
短标题：Metrics Aggregation
难度：intermediate
子主题：Metrics和Alerting

## 中文导读

本题要求你完成 `实现 Metrics Aggregation和Rollups`。

重点关注：`aggregation`、`rollup`、`sum`、`average`、`percentile`。

建议先按提示逐步实现：sum: add all values across services or instances。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Individual data points are too granular用于dashboards和alerting. Aggregation reduces them to meaningful summaries: totals across services, averages across instances,和time rollups that compress many data points into periodic buckets.

Implement a 节点 that performs metric aggregations:

```JSON
// Sum requests across services, grouped by service name
{ "type": "aggregate_metric", "msg_id": 1,
  "metric": "http_requests_total", "aggregator": "sum",
  "group_by": ["service"],
  "services": ["api","web","auth"], "time_range": "1h" }
-> { "type": "aggregation_result", "in_reply_to": 1,
    "results": [{"service":"api","value":50000},
                 {"service":"web","value":30000},
                 {"service":"auth","value":15000}],
    "total": 95000 }

// Average memory across three instances
{ "type": "aggregate_metric", "msg_id": 2,
  "metric": "memory_usage_bytes", "aggregator": "avg",
  "values": [1073741824, 2147483648, 1610612736] }
-> { "type": "aggregation_result", "in_reply_to": 2,
    "value": 1610612736, "unit": "bytes", "sample_count": 3 }
```

## 涉及概念

- `aggregation`
- `rollup`
- `sum`
- `average`
- `percentile`
- `time buckets`

## 实现提示

- sum: add all values across services or instances
- avg: total sum / count of values
- rollup: group data points by time interval, then compute aggregations within each bucket
- p95: sort all values, return the one at 索引 floor(0.95 * count)
- total in a sum aggregation is the grand total across all groups

## 测试用例

### 1. Sum aggregation across services

Should sum requests per service和compute grand total 95000.

输入：

```json
{"src":"query","dest":"metrics","body":{"type":"aggregate_metric","msg_id":1,"metric":"http_requests_total","aggregator":"sum","group_by":["service"],"services":["api","web","auth"],"time_range":"1h"}}
```

期望输出：

```text
{"type": "aggregation_result", "in_reply_to": 1, "results": [{"service": "api", "value": 50000}, {"service": "web", "value": 30000}, {"service": "auth", "value": 15000}], "total": 95000}
```

### 2. Average aggregation

Average of three memory values should be 1610612736 bytes.

输入：

```json
{"src":"query","dest":"metrics","body":{"type":"aggregate_metric","msg_id":1,"metric":"memory_usage_bytes","aggregator":"avg","instances":["api-1","api-2","api-3"],"values":[1073741824,2147483648,1610612736]}}
```

期望输出：

```text
{"type": "aggregation_result", "in_reply_to": 1, "value": 1610612736, "unit": "bytes", "sample_count": 3}
```

## 参考资料

- [PromQL Aggregation](https://prometheus.io/docs/prometheus/latest/querying/basics/)：Prometheus query language aggregation operators

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
