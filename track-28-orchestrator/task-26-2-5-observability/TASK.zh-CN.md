# 实现 服务 Mesh Observability

英文标题：Implement Service Mesh Observability
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-5-observability>

课程：28. 编排器：容器调度与服务网格
任务序号：10
短标题：Observability
难度：intermediate
子主题：服务 Mesh

## 中文导读

本题要求你完成 `实现 服务 Mesh Observability`。

重点关注：`metrics`、`distributed tracing`、`access logs`、`service graph`、`golden signals`。

建议先按提示逐步实现：record stores one 请求 metric: service name, duration_ms,和HTTP status code。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Observability in a service mesh means collecting metrics, traces,和logs from every sidecar 代理 automatically, without changing application code. The three pillars together let you understand what is happening和diagnose problems quickly.

Implement a 节点 that handles all three observability signals:

```JSON
// Record a 请求 metric (latency + status code)
{ "type": "record", "msg_id": 1,
  "service": "api", "duration_ms": 150, "status": 200 }
-> { "type": "metrics_recorded", "in_reply_to": 1,
    "service": "api", "request_count": 1 }

// Create a distributed trace，包含a span
{ "type": "trace", "msg_id": 2,
  "operation": "GET /api/users" }
-> { "type": "trace_created", "in_reply_to": 2,
    "trace_id": "<uuid>", "span_id": "<uuid>" }

// Query access logs by service
{ "type": "query", "msg_id": 3,
  "filter": {"source_service": "api", "target_service": "database"} }
-> { "type": "access_logs", "in_reply_to": 3,
    "logs": [{"source_service": "api", "target_service": "database", "count": 50}] }

// Generate service dependency graph
{ "type": "generate", "msg_id": 4 }
-> { "type": "service_graph", "in_reply_to": 4,
    "节点": ["api", "database", "缓存"],
    "edges": [{"source": "api", "target": "database", "request_count": 500}] }
```

## 涉及概念

- `metrics`
- `distributed tracing`
- `access logs`
- `service graph`
- `golden signals`

## 实现提示

- record stores one 请求 metric: service name, duration_ms,和HTTP status code
- trace creates a trace，包含a unique trace_id和a span用于the given operation
- query returns access logs filtered by source_service and/or target_service
- generate builds a service graph: 节点 are service names, edges are (source, target, count) pairs
- request_count increments by 1用于every record call用于that service

## 测试用例

### 1. Collect 服务 metrics

Should record the metric和return the updated 请求 count.

输入：

```json
{"src":"sidecar","dest":"metrics","body":{"type":"record","msg_id":1,"service":"api","duration_ms":150,"status":200}}
```

期望输出：

```text
{"type": "metrics_recorded", "in_reply_to": 1, "service": "api", "request_count": 1}
```

### 2. 创建 distributed trace

Should create a trace，包含unique trace_id和span_id.

输入：

```json
{"src":"service-a","dest":"tracer","body":{"type":"trace","msg_id":1,"operation":"GET /api/users"}}
```

期望输出：

```text
{"type": "trace_created", "in_reply_to": 1, "trace_id": ".*", "span_id": ".*"}
```

## 参考资料

- [Observability in a Service Mesh](https://istio.io/latest/docs/concepts/observability/)：How Istio collects metrics, traces,和logs from sidecars

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
