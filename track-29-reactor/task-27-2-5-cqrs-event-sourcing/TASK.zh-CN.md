# 实现 CQRS，包含Event Sourcing

英文标题：Implement CQRS，包含Event Sourcing
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-5-cqrs-event-sourcing>

课程：29. 反应器：事件溯源与 CQRS
任务序号：10
短标题：CQRS + Event Sourcing
难度：advanced
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你完成 `实现 CQRS，包含Event Sourcing`。

重点关注：`CQRS`、`event sourcing`、`aggregate`、`projection`、`temporal query`。

建议先按提示逐步实现：Commands go through validation, then are applied to the aggregate, which emits events。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

CQRS和event sourcing are designed to work together: commands write to the event store (the source of truth),和projections built from those events serve queries. This gives you the full audit trail of event sourcing plus the read performance of CQRS.

Implement a 节点 that integrates both patterns end-to-end:

```JSON
// Command: validate, apply to aggregate, persist event, update projections
{ "type": "command", "msg_id": 1,
  "command": {"type": "CreateUser",
               "payload": {"id": "user-123", "name": "John"}} }
-> { "type": "command_result", "in_reply_to": 1,
    "success": true,
    "events": [{"eventType": "UserCreated", "aggregateId": "user-123"}] }

// Query: read from projection (never from event store)
{ "type": "query", "msg_id": 2,
  "query": {"type": "GetUser", "params": {"userId": "user-123"}} }
-> { "type": "query_result", "in_reply_to": 2,
    "data": {"id": "user-123", "name": "John"} }

// Temporal query: replay event store up to a point in time
{ "type": "query", "msg_id": 3,
  "query": {"type": "GetUserAtTime",
             "params": {"userId": "user-123",
                        "timestamp": "2024-01-15T09:00:00Z"}} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": {"id": "user-123", "name": "John Doe",
             "at_time": "2024-01-15T09:00:00Z"} }
```

The flow用于a command is: validate -> apply to aggregate -> append event to store -> update projections. The flow用于a query is: read from projection (for current state) or replay event store (for past state).

## 涉及概念

- `CQRS`
- `event sourcing`
- `aggregate`
- `projection`
- `temporal query`
- `full-stack integration`

## 实现提示

- Commands go through validation, then are applied to the aggregate, which emits events
- Events are stored in the event store和then applied to projections
- Queries read from projections, not from the event store directly
- Temporal queries replay the event store up to a given timestamp
- The aggregate version must match the expected version on every command (optimistic locking)

## 测试用例

### 1. Execute command，包含event sourcing

Command should emit a UserCreated event，包含the correct aggregateId.

输入：

```json
{"src":"client","dest":"cqrs","body":{"type":"command","msg_id":1,"command":{"type":"CreateUser","payload":{"id":"user-123","name":"John"}}}}
```

期望输出：

```text
{"type": "command_result", "in_reply_to": 1, "success": true, "events": [{"eventType": "UserCreated", "aggregateId": "user-123"}]}
```

### 2. Query from projection

Query should read from the projection, not the event store.

输入：

```json
{"src":"client","dest":"cqrs","body":{"type":"query","msg_id":1,"query":{"type":"GetUser","params":{"userId":"user-123"}}}}
```

期望输出：

```text
{"type": "query_result", "in_reply_to": 1, "data": {"id": "user-123", "name": "John"}}
```

## 参考资料

- [CQRS和Event Sourcing](https://martinfowler.com/bliki/CQRS.html)：Combining CQRS，包含event sourcing用于full auditability和read performance

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
