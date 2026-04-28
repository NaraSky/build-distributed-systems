# 实现 Metrics Collection

英文标题：Implement Metrics Collection
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-1-metrics-collection>

课程：25. 追踪器：可观测性
任务序号：6
短标题：Metrics Collection
难度：intermediate
子主题：Metrics和Alerting

## 中文导读

本题要求你完成 `实现 Metrics Collection`。

重点关注：`counter`、`gauge`、`histogram`、`labels`、`percentile`。

建议先按提示逐步实现：计数器: only increases — use用于请求 counts, error counts, bytes sent。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Metrics quantify system behavior: how many requests, how fast, how much memory. Three types cover nearly everything: counters (monotonically increasing), gauges (can go up or down),和histograms (distribution of values like 请求 duration).

Implement a 节点 that records和queries metrics:

```JSON
// 计数器: increment by 1 on each 请求
{ "type": "计数器", "msg_id": 1,
  "name": "http_requests_total", "value": 1,
  "labels": {"method": "POST", "service": "api"} }
-> { "type": "metric_recorded", "in_reply_to": 1,
    "name": "http_requests_total", "value": 1 }

// Gauge: current heap memory in bytes
{ "type": "gauge", "msg_id": 2,
  "name": "memory_usage_bytes", "value": 1073741824,
  "labels": {"service": "api", "type": "heap"} }
-> { "type": "metric_recorded", "in_reply_to": 2,
    "name": "memory_usage_bytes", "value": 1073741824 }

// Histogram: record one 请求 duration observation
{ "type": "histogram", "msg_id": 3,
  "name": "request_duration_ms", "value": 123,
  "labels": {"endpoint": "/api/users"} }
-> { "type": "metric_recorded", "in_reply_to": 3,
    "name": "request_duration_ms", "count": 1, "sum": 123 }
```

## 涉及概念

- `counter`
- `gauge`
- `histogram`
- `labels`
- `percentile`

## 实现提示

- 计数器: only increases — use用于请求 counts, error counts, bytes sent
- Gauge: can go up or down — use用于memory usage, 队列 depth, connection count
- Histogram: records value distribution — use用于请求 duration, 响应 size
- Labels are key-value pairs that add dimensions (filter by service, endpoint, status)
- p95 = value at the 95th percentile: 95% of requests complete faster than this

## 测试用例

### 1. 计数器 metric

计数器 should record和acknowledge the increment.

输入：

```json
{"src":"service","dest":"metrics","body":{"type":"counter","msg_id":1,"name":"http_requests_total","value":1,"labels":{"method":"POST","service":"api"}}}
```

期望输出：

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "http_requests_total", "value": 1}
```

### 2. Gauge metric

Gauge should record the current value.

输入：

```json
{"src":"service","dest":"metrics","body":{"type":"gauge","msg_id":1,"name":"memory_usage_bytes","value":1073741824,"labels":{"service":"api","type":"heap"}}}
```

期望输出：

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "memory_usage_bytes", "value": 1073741824}
```

### 3. Histogram metric

Histogram should record value和update count和sum.

输入：

```json
{"src":"service","dest":"metrics","body":{"type":"histogram","msg_id":1,"name":"request_duration_ms","value":123,"labels":{"endpoint":"/api/users"}}}
```

期望输出：

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "request_duration_ms", "count": 1, "sum": 123}
```

## 参考资料

- [Prometheus Metric Types](https://prometheus.io/docs/concepts/metric_types/)：计数器, gauge, histogram,和summary metric types explained

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
