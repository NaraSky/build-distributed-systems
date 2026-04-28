# 实现跨度生命周期管理

英文标题：Implement Span Lifecycle Management
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-2-span-lifecycle>

课程：25. 追踪器：可观测性
任务序号：2
短标题：Span Lifecycle
难度：进阶
子主题：Distributed Tracing

## 中文导读

这道题要求你管理跨度（Span）的完整生命周期：从创建、记录事件，到结束并计算耗时。跨度是分布式追踪中的基本单元，代表一次操作的执行过程。掌握跨度的生命周期管理，是构建追踪系统的关键一步。

## 题目说明

跨度（Span）代表一条追踪中的一个操作。它包含名称、开始和结束时间戳、状态，还可以选择性地包含事件和链接。跨度类型（Span Kind）用来标识这个操作是收到的服务端调用、发出的客户端调用，还是内部处理。

请实现一个节点来管理跨度的生命周期：

```json
// 完整生命周期：创建 -> 记录事件 -> 结束
{ "type": "create_span", "msg_id": 1, "name": "GET /api/users/123" }
{ "type": "span_event", "span_id": "span1", "event": "db.query" }
{ "type": "span_end", "span_id": "span1", "status": "OK" }
-> { "type": "span_complete",
    "span_id": "span1", "duration_us": 10000, "status": "OK" }

// 跨度执行过程中出错 -> 标记为 ERROR 状态
{ "type": "create_span", "msg_id": 2, "name": "GET /api/users/999" }
{ "type": "span_error", "span_id": "span2", "error": "User not found" }
-> { "type": "span_complete",
    "span_id": "span2", "status": "ERROR", "error": "User not found" }

// CLIENT 类型表示对外发起的调用
{ "type": "create_span", "msg_id": 3,
  "name": "GET /api/data", "kind": "CLIENT" }
-> { "type": "span_created", "span_id": "span1", "kind": "CLIENT" }
```

## 概念说明

可以把**跨度**想象成一个秒表：你按下"开始"记录一个操作的起点，中间可以打若干个"标记"（事件），最后按下"停止"就得到了这次操作的耗时和状态。**跨度类型**则告诉你这个操作的角色——是在响应别人的请求（SERVER），还是在调用别人的服务（CLIENT）。

## 涉及概念

- `span lifecycle`
- `span kind`
- `span events`
- `span links`
- `duration`

## 实现提示

- 跨度在收到 create_span 时开始，在收到 span_end 时结束；耗时 = 结束时间 - 开始时间
- 默认状态为 OK；span_error 会将状态设置为 ERROR 并附带错误信息
- 跨度类型：SERVER 表示收到的请求，CLIENT 表示发出的对外调用
- 跨度事件是跨度内部带时间戳的瞬时标注
- 跨度链接用于关联不直接具有父子关系的相关跨度

## 测试用例

### 1. 跨度生命周期流转

跨度应当跟踪从开始到结束的过程，并计算耗时。

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

### 2. 带错误状态的跨度

span_error 应当将状态设置为 ERROR 并附带错误信息。

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

- [OpenTelemetry Trace Spec](https://opentelemetry.io/docs/concepts/signals/traces/)：OpenTelemetry 关于跨度和追踪的规范说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
