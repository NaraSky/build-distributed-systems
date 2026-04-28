# 实现分布式追踪上下文传播

英文标题：Implement Distributed Trace Context Propagation
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-1-trace-context-propagation>

课程：25. 追踪器：可观测性
任务序号：1
短标题：Trace Propagation
难度：进阶
子主题：Distributed Tracing

## 中文导读

这道题要求你实现分布式追踪（Distributed Tracing）中的上下文传播机制。当一个请求在多个服务之间流转时，每个服务需要把"追踪上下文"（包含追踪标识和父级跨度标识）通过请求头传递下去，这样才能把所有环节串成一棵完整的调用树。理解这个机制是掌握分布式系统可观测性的基础。

## 题目说明

分布式追踪（Distributed Tracing）的核心思想是：把一个请求在多个服务间产生的跨度（Span）串联起来。每个服务在处理请求时，会通过请求头传播追踪上下文（Trace Context），其中包含追踪标识（Trace ID）和父级跨度标识（Parent Span ID），这样所有环节就能被组装成一棵完整的追踪树（Trace Tree）。

请实现一个节点，处理以下追踪上下文操作：

```json
// 服务 B 收到带有 traceparent 头的请求 -> 创建子跨度
{ "type": "http_request", "msg_id": 1, "path": "/api/data",
  "headers": {"traceparent": "00-trace123-span_a-01"} }
-> { "type": "http_response", "in_reply_to": 1,
    "span": {"trace_id": "trace123", "span_id": "span_b",
              "parent_span_id": "span_a"} }

// 解析 W3C traceparent 头，拆分为各个组成部分
{ "type": "parse_traceparent", "msg_id": 2,
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b57-01" }
-> { "type": "parse_ok", "in_reply_to": 2,
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "parent_span_id": "00f067aa0ba902b57", "sampled": true }

// 根据跨度列表重建追踪树
{ "type": "reconstruct_trace", "msg_id": 3,
  "spans": [{"trace_id":"t1","span_id":"s1","parent":null},
             {"trace_id":"t1","span_id":"s2","parent":"s1"},
             {"trace_id":"t1","span_id":"s3","parent":"s2"}] }
-> { "type": "trace_tree_ok", "in_reply_to": 3,
    "trace_id": "t1", "span_count": 3, "depth": 3 }
```

## 概念说明

**分布式追踪**就像给请求贴上一个全局身份证号。想象你在网上下单，这个请求会经过网关、订单服务、支付服务、库存服务等多个环节。分布式追踪让你能看到这个请求在每个环节花了多少时间、是否出错。

**W3C traceparent** 是一种标准化的请求头格式，格式为 `00-{追踪标识}-{父跨度标识}-{标志位}`。就像快递单号一样，每个服务看到这个头就知道当前请求属于哪条追踪链路。

## 涉及概念

- `distributed tracing`
- `trace context`
- `W3C traceparent`
- `span`
- `trace tree`

## 实现提示

- W3C traceparent 的格式为：`00-{trace_id}-{parent_span_id}-{flags}`
- 当服务 B 收到带有 traceparent 头的请求时，需要创建一个子跨度，其 parent_span_id 取自该头部
- 采样标志位：最后一个字节为 01 表示已采样，00 表示未采样
- 生成 traceparent 时，格式为 `00-{trace_id}-{span_id}-01`
- 追踪树的深度等于最长的父子链的长度

## 测试用例

### 1. 传播追踪上下文

服务 B 应当提取追踪上下文并创建一个子跨度。

输入：

```json
{"src":"service_a","dest":"service_b","body":{"type":"http_request","msg_id":1,"path":"/api/data","headers":{"traceparent":"00-trace123-span_a-01"}}}
```

期望输出：

```text
{"src": "service_b", "dest": "service_a", "body": {"type": "http_response", "in_reply_to": 1, "span": {"trace_id": "trace123", "span_id": "span_b", "parent_span_id": "span_a"}}}
```

### 2. 解析 W3C traceparent 头

应当将 traceparent 解析为 trace_id、parent_span_id 和采样标志位。

输入：

```json
{"src":"service","dest":"parser","body":{"type":"parse_traceparent","msg_id":1,"traceparent":"00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b57-01"}}
```

期望输出：

```text
{"src": "parser", "dest": "service", "body": {"type": "parse_ok", "in_reply_to": 1, "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736", "parent_span_id": "00f067aa0ba902b57", "sampled": true}}
```

## 参考资料

- [W3C Trace Context](https://www.w3.org/TR/trace-context/)：W3C 制定的分布式追踪上下文传播标准

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
