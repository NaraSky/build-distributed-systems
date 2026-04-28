# Implement Metrics Aggregation and Rollups

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-2-3-metrics-aggregation>

Track: 25. The Tracer
Task order: 8
Short title: Metrics Aggregation
Difficulty: intermediate
Subtrack: Metrics and Alerting

## Problem

Individual data points are too granular for dashboards and alerting. Aggregation reduces them to meaningful summaries: totals across services, averages across instances, and time rollups that compress many data points into periodic buckets.

Implement a node that performs metric aggregations:

```json
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

## Concepts

- aggregation
- rollup
- sum
- average
- percentile
- time buckets

## Hints

- sum: add all values across services or instances
- avg: total sum / count of values
- rollup: group data points by time interval, then compute aggregations within each bucket
- p95: sort all values, return the one at index floor(0.95 * count)
- total in a sum aggregation is the grand total across all groups

## Test Cases

### 1. Sum aggregation across services

Should sum requests per service and compute grand total 95000.

Input:

```json
{"src":"query","dest":"metrics","body":{"type":"aggregate_metric","msg_id":1,"metric":"http_requests_total","aggregator":"sum","group_by":["service"],"services":["api","web","auth"],"time_range":"1h"}}
```

Expected output:

```text
{"type": "aggregation_result", "in_reply_to": 1, "results": [{"service": "api", "value": 50000}, {"service": "web", "value": 30000}, {"service": "auth", "value": 15000}], "total": 95000}
```

### 2. Average aggregation

Average of three memory values should be 1610612736 bytes.

Input:

```json
{"src":"query","dest":"metrics","body":{"type":"aggregate_metric","msg_id":1,"metric":"memory_usage_bytes","aggregator":"avg","instances":["api-1","api-2","api-3"],"values":[1073741824,2147483648,1610612736]}}
```

Expected output:

```text
{"type": "aggregation_result", "in_reply_to": 1, "value": 1610612736, "unit": "bytes", "sample_count": 3}
```

## Resources

- [PromQL Aggregation](https://prometheus.io/docs/prometheus/latest/querying/basics/): Prometheus query language aggregation operators

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
