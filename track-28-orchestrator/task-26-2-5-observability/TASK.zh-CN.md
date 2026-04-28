# 实现服务网格可观测性

英文标题：Implement Service Mesh Observability
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-5-observability>

课程：28. 编排器：容器调度与服务网格
任务序号：10
短标题：Observability
难度：进阶
子主题：Service Mesh

## 中文导读

这道题要求你实现一个处理三大可观测性信号的节点。服务网格中的可观测性（Observability）意味着自动从每个边车代理收集指标、追踪和日志，无需修改应用代码。这三大支柱结合在一起，让你能快速了解系统正在发生什么、诊断问题出在哪里。可以把它想象成给你的分布式系统装上了"透视眼"和"心电图"。

## 题目说明

服务网格中的可观测性意味着自动从每个边车代理收集指标（Metrics）、追踪（Traces）和日志（Logs），无需修改应用代码。这三大支柱结合在一起，让你能了解系统正在发生什么，并快速诊断问题。

请实现一个处理三大可观测性信号的节点：

```json
// 记录一个请求指标（延迟 + 状态码）
{ "type": "record", "msg_id": 1,
  "service": "api", "duration_ms": 150, "status": 200 }
-> { "type": "metrics_recorded", "in_reply_to": 1,
    "service": "api", "request_count": 1 }

// 创建一个分布式追踪及其调用段
{ "type": "trace", "msg_id": 2,
  "operation": "GET /api/users" }
-> { "type": "trace_created", "in_reply_to": 2,
    "trace_id": "<uuid>", "span_id": "<uuid>" }

// 按服务查询访问日志
{ "type": "query", "msg_id": 3,
  "filter": {"source_service": "api", "target_service": "database"} }
-> { "type": "access_logs", "in_reply_to": 3,
    "logs": [{"source_service": "api", "target_service": "database", "count": 50}] }

// 生成服务依赖关系图
{ "type": "generate", "msg_id": 4 }
-> { "type": "service_graph", "in_reply_to": 4,
    "nodes": ["api", "database", "cache"],
    "edges": [{"source": "api", "target": "database", "request_count": 500}] }
```

## 涉及概念

- `metrics`
- `distributed tracing`
- `access logs`
- `service graph`
- `golden signals`

## 实现提示

- `record` 存储一条请求指标：服务名称、耗时和 HTTP 状态码
- `trace` 创建一个包含唯一 `trace_id` 和调用段（Span）的追踪
- `query` 返回按源服务和目标服务过滤的访问日志
- `generate` 构建服务依赖关系图：节点是服务名称，边是（源服务、目标服务、请求数量）的组合
- 每次调用 `record` 时，对应服务的 `request_count` 递增 1

## 测试用例

### 1. 收集服务指标

应记录指标并返回更新后的请求计数。

输入：

```json
{"src":"sidecar","dest":"metrics","body":{"type":"record","msg_id":1,"service":"api","duration_ms":150,"status":200}}
```

期望输出：

```text
{"type": "metrics_recorded", "in_reply_to": 1, "service": "api", "request_count": 1}
```

### 2. 创建分布式追踪

应创建一个包含唯一 trace_id 和 span_id 的追踪。

输入：

```json
{"src":"service-a","dest":"tracer","body":{"type":"trace","msg_id":1,"operation":"GET /api/users"}}
```

期望输出：

```text
{"type": "trace_created", "in_reply_to": 1, "trace_id": ".*", "span_id": ".*"}
```

## 参考资料

- [Observability in a Service Mesh](https://istio.io/latest/docs/concepts/observability/)：Istio 如何从边车代理自动收集指标、追踪和日志

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
