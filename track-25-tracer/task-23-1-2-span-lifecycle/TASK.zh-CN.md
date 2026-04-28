# 实现 Span Lifecycle Management

英文标题：Implement Span Lifecycle Management
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-2-span-lifecycle>

课程：25. 追踪器：可观测性
任务序号：2
短标题：Span Lifecycle
难度：intermediate
子主题：Distributed Tracing

## 中文导读

本题要求你完成 `实现 Span Lifecycle Management`。

重点关注：`span lifecycle`、`span kind`、`span events`、`span links`、`duration`。

建议先按提示逐步实现：Span starts on create_span和ends on span_end; duration = end_time - start_time。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A span represents one operation within a trace: it has a name, start和end timestamps, status,和optionally events和links. The span kind identifies whether the operation is an incoming 服务端 call, an outgoing 客户端 call, or internal work.

Implement a 节点 that manages span lifecycles:

```JSON
// Full lifecycle: create -> event -> end
{ "type": "create_span", "msg_id": 1, "name": "GET /api/users/123" }
{ "type": "span_event", "span_id": "span1", "event": "db.query" }
{ "type": "span_end", "span_id": "span1", "status": "OK" }
-> { "type": "span_complete",
    "span_id": "span1", "duration_us": 10000, "status": "OK" }

// Error during span -> ERROR status
{ "type": "create_span", "msg_id": 2, "name": "GET /api/users/999" }
{ "type": "span_error", "span_id": "span2", "error": "User not found" }
-> { "type": "span_complete",
    "span_id": "span2", "status": "ERROR", "error": "User not found" }

// 客户端 kind用于outbound calls
{ "type": "create_span", "msg_id": 3,
  "name": "GET /api/data", "kind": "客户端" }
-> { "type": "span_created", "span_id": "span1", "kind": "客户端" }
```

## 涉及概念

- `span lifecycle`
- `span kind`
- `span events`
- `span links`
- `duration`

## 实现提示

- Span starts on create_span和ends on span_end; duration = end_time - start_time
- Default status is OK; span_error sets status=ERROR，包含the error 消息
- Span kind: 服务端用于incoming requests, 客户端用于outbound calls to other services
- Span events are timestamped point-in-time annotations inside a span
- Span links connect related spans that are not in a direct parent-child relationship

## 测试用例

### 1. Span lifecycle progression

Span should track start to end和calculate duration.

输入：

```json
{"src":"service","dest":"tracer","body":{"type":"create_span","msg_id":1,"name":"GET /api/users/123"}}
{"type":"span_event","span_id":"span1","event":"db.query"}
{"type":"span_end","span_id":"span1","status":"OK"}
```

期望输出：

```text
{"src": "tracer", "dest": "service", "body": {"type": "span_complete", "span_id": "span1", "duration_us": 10000, "status": "OK"}}
```

### 2. Span，包含error status

span_error should set status=ERROR，包含the error 消息.

输入：

```json
{"src":"service","dest":"tracer","body":{"type":"create_span","msg_id":1,"name":"GET /api/users/999"}}
{"type":"span_error","span_id":"span2","error":"User not found"}
```

期望输出：

```text
{"src": "tracer", "dest": "service", "body": {"type": "span_complete", "span_id": "span2", "status": "ERROR", "error": "User not found"}}
```

## 参考资料

- [OpenTelemetry Trace Spec](https://opentelemetry.io/docs/concepts/signals/traces/)：OpenTelemetry specification用于spans和traces

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
