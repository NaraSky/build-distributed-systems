# Implement Metrics Collection

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-1-metrics-collection>

Track: 25. The Tracer
Task order: 6
Short title: Metrics Collection
Difficulty: intermediate
Subtrack: Metrics and Alerting

## Problem

Metrics quantify system behavior: how many requests, how fast, how much memory. Three types cover nearly everything: counters (monotonically increasing), gauges (can go up or down), and histograms (distribution of values like request duration).

Implement a node that records and queries metrics:

```json
// Counter: increment by 1 on each request
{ "type": "counter", "msg_id": 1,
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

// Histogram: record one request duration observation
{ "type": "histogram", "msg_id": 3,
  "name": "request_duration_ms", "value": 123,
  "labels": {"endpoint": "/api/users"} }
-> { "type": "metric_recorded", "in_reply_to": 3,
    "name": "request_duration_ms", "count": 1, "sum": 123 }
```

## Concepts

- counter
- gauge
- histogram
- labels
- percentile

## Hints

- Counter: only increases — use for request counts, error counts, bytes sent
- Gauge: can go up or down — use for memory usage, queue depth, connection count
- Histogram: records value distribution — use for request duration, response size
- Labels are key-value pairs that add dimensions (filter by service, endpoint, status)
- p95 = value at the 95th percentile: 95% of requests complete faster than this

## Test Cases

### 1. Counter metric

Counter should record and acknowledge the increment.

Input:

```json
{"src":"service","dest":"metrics","body":{"type":"counter","msg_id":1,"name":"http_requests_total","value":1,"labels":{"method":"POST","service":"api"}}}
```

Expected output:

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "http_requests_total", "value": 1}
```

### 2. Gauge metric

Gauge should record the current value.

Input:

```json
{"src":"service","dest":"metrics","body":{"type":"gauge","msg_id":1,"name":"memory_usage_bytes","value":1073741824,"labels":{"service":"api","type":"heap"}}}
```

Expected output:

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "memory_usage_bytes", "value": 1073741824}
```

### 3. Histogram metric

Histogram should record value and update count and sum.

Input:

```json
{"src":"service","dest":"metrics","body":{"type":"histogram","msg_id":1,"name":"request_duration_ms","value":123,"labels":{"endpoint":"/api/users"}}}
```

Expected output:

```text
{"type": "metric_recorded", "in_reply_to": 1, "name": "request_duration_ms", "count": 1, "sum": 123}
```

## Resources

- [Prometheus Metric Types](https://prometheus.io/docs/concepts/metric_types/): Counter, gauge, histogram, and summary metric types explained

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
