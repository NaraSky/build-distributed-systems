# 实现 Event Projections

英文标题：Implement Event Projections
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-4-event-projections>

课程：29. 反应器：事件溯源与 CQRS
任务序号：4
短标题：Event Projections
难度：intermediate
子主题：Event Sourcing

## 中文导读

本题要求你完成 `实现 Event Projections`。

重点关注：`projections`、`read models`、`event-driven denormalization`、`rebuild`、`versioned projection`。

建议先按提示逐步实现：A projection is a named read model built by consuming events one at a time。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The event store is optimized用于writes, not queries. A **projection** solves this: it listens to the event stream和maintains a denormalized read model that is fast to query. When the event schema changes or a new view is needed, the projection can be rebuilt from scratch.

Implement a 节点 that manages named projections:

```JSON
// Create a new projection，包含an initial empty state
{ "type": "create", "msg_id": 1,
  "name": "user-listing", "initial_state": [] }
-> { "type": "projection_created", "in_reply_to": 1,
    "name": "user-listing", "version": 0 }

// Apply one event to a projection
{ "type": "update", "msg_id": 2,
  "projection": "user-listing",
  "event": {"event_type": "UserCreated",
             "event_data": {"id": "user-123", "name": "John"}} }
-> { "type": "projection_updated", "in_reply_to": 2,
    "projection": "user-listing", "version": 1,
    "state": [{"id": "user-123", "name": "John"}] }

// Rebuild projection from scratch使用a list of past events
{ "type": "rebuild", "msg_id": 3,
  "projection": "user-listing",
  "events": [{"event_type": "UserCreated", "event_data": {"id": "user-123"}}] }
-> { "type": "projection_rebuilt", "in_reply_to": 3,
    "projection": "user-listing",
    "events_processed": 1, "version": 1 }
```

The projection version increments by 1用于every event applied. Rebuilding resets the version to 0和replays all supplied events.

## 涉及概念

- `projections`
- `read models`
- `event-driven denormalization`
- `rebuild`
- `versioned projection`

## 实现提示

- A projection is a named read model built by consuming events one at a time
- create initializes a projection，包含an empty state和version 0
- update applies one event to the projection和increments its version
- rebuild replays a list of events from scratch onto the projection
- Each update/rebuild step should merge event_data into the projection state

## 测试用例

### 1. 创建 listing projection

Should create new projection at version 0.

输入：

```json
{"src":"projector","dest":"projection","body":{"type":"create","msg_id":1,"name":"user-listing","initial_state":[]}}
```

期望输出：

```text
{"type": "projection_created", "in_reply_to": 1, "name": "user-listing", "version": 0}
```

### 2. Update projection，包含event

Should append user to listing和increment version to 1.

输入：

```json
{"src":"eventstore","dest":"projection","body":{"type":"update","msg_id":1,"projection":"user-listing","event":{"event_type":"UserCreated","event_data":{"id":"user-123","name":"John"}}}}
```

期望输出：

```text
{"type": "projection_updated", "in_reply_to": 1, "projection": "user-listing", "version": 1, "state": [{"id": "user-123", "name": "John"}]}
```

## 参考资料

- [Projections in Event Sourcing](https://eventstore.com/blog/projections/)：How projections turn events into query-optimized read models

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
