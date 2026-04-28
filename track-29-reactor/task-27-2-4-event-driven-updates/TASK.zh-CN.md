# 实现 Event-Driven Read模式l Updates

英文标题：Implement Event-Driven Read模式l Updates
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-4-event-driven-updates>

课程：29. 反应器：事件溯源与 CQRS
任务序号：9
短标题：Event-Driven Updates
难度：intermediate
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你完成 `实现 Event-Driven Read模式l Updates`。

重点关注：`event bus`、`projector`、`subscription`、`idempotent updates`、`eventual consistency`。

建议先按提示逐步实现：subscribe registers the projector to receive the listed event types from the event bus。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In CQRS, the command side emits events和the query side must react to those events to keep its read models up-to-date. An **event-driven projector** subscribes to the event bus和updates one or more read models whenever a relevant event arrives.

Implement a 节点 that acts as a projector，包含subscription和idempotent update support:

```JSON
// Register interest in specific event types
{ "type": "subscribe", "msg_id": 1,
  "event_types": ["UserCreated", "UserUpdated"] }
-> { "type": "subscribed", "in_reply_to": 1,
    "event_types": ["UserCreated", "UserUpdated"] }

// Event arrives: update all relevant read models
{ "type": "event", "msg_id": 2,
  "event": {"type": "UserCreated",
             "payload": {"id": "user-123", "name": "John"}} }
-> { "type": "read_models_updated", "in_reply_to": 2,
    "event_id": "evt-123",
    "updated_models": ["user_listing", "user_by_email"] }

// Same event_id arrives again: skip it
{ "type": "event", "msg_id": 3,
  "event": {"type": "UserCreated", "id": "evt-123",
             "payload": {"id": "user-123"}} }
-> { "type": "event_skipped", "in_reply_to": 3,
    "event_id": "evt-123", "reason": "already_processed" }
```

Idempotency is critical: the event bus may deliver the same event more than once. Always check the event_id before applying any update.

## 涉及概念

- `event bus`
- `projector`
- `subscription`
- `idempotent updates`
- `eventual consistency`

## 实现提示

- subscribe registers the projector to receive the listed event types from the event bus
- When an event arrives, update every read model that cares about that event type
- Track processed event IDs; return event_skipped用于duplicates (idempotency)
- updated_models lists the names of all read models that were actually updated
- 最终一致性: read models may lag slightly behind the write model

## 测试用例

### 1. Subscribe to events

Should acknowledge subscription to both event types.

输入：

```json
{"src":"projector","dest":"eventbus","body":{"type":"subscribe","msg_id":1,"event_types":["UserCreated","UserUpdated"]}}
```

期望输出：

```text
{"type": "subscribed", "in_reply_to": 1, "event_types": ["UserCreated", "UserUpdated"]}
```

### 2. Update read models on event

UserCreated should update both user_listing和user_by_email read models.

输入：

```json
{"src":"eventbus","dest":"projector","body":{"type":"event","msg_id":1,"event":{"type":"UserCreated","payload":{"id":"user-123","name":"John"}}}}
```

期望输出：

```text
{"type": "read_models_updated", "in_reply_to": 1, "event_id": "evt-123", "updated_models": ["user_listing", "user_by_email"]}
```

## 参考资料

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)：Event-driven read model updates in CQRS

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
