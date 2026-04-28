# 实现 Event 存储

英文标题：Implement Event Store
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-1-event-store>

课程：29. 反应器：事件溯源与 CQRS
任务序号：1
短标题：Event 存储
难度：intermediate
子主题：Event Sourcing

## 中文导读

本题要求你完成 `实现 Event 存储`。

重点关注：`event sourcing`、`append-only log`、`optimistic concurrency`、`aggregate`、`sequence number`。

建议先按提示逐步实现：Events are immutable — never update or delete, only append。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

An event store is an **append-only 日志** where every change to an aggregate is recorded as an immutable event. To reconstruct current state you replay all events in order — or start from a snapshot. Overwriting state is never allowed.

Implement a 节点 that manages events用于multiple aggregates，包含**optimistic concurrency control**: the caller declares which version they expect; if another writer already changed the aggregate, the append is rejected.

```JSON
// Append an event (version must match current aggregate version)
{ "type": "append", "msg_id": 1,
  "aggregate_id": "user-123", "event_type": "UserCreated",
  "event_data": {"name": "John"}, "version": 0 }
-> { "type": "appended", "in_reply_to": 1,
    "event_id": "<uuid>", "sequence_number": 1 }

// Version mismatch -> reject
{ "type": "append", "version": 5 }   // actual version is 0
-> { "type": "concurrency_error", "in_reply_to": 1,
    "error": "Expected version 5, got 0" }

// Save a snapshot at the aggregate's current version
{ "type": "create_snapshot", "msg_id": 3, "aggregate_id": "user-123" }
-> { "type": "snapshot_created", "in_reply_to": 3,
    "aggregate_id": "user-123", "version": 1 }
```

Each aggregate starts at version 0. Every successful append increments its version by 1和advances the global sequence number.

## 涉及概念

- `event sourcing`
- `append-only log`
- `optimistic concurrency`
- `aggregate`
- `sequence number`
- `snapshot`

## 实现提示

- Events are immutable — never update or delete, only append
- Track a version per aggregate; reject appends where the sent version does not match current
- Sequence numbers are global和monotonically increasing across all aggregates
- A snapshot stores the aggregate state at a specific version to speed up replay
- Return a generated event_id和the new sequence_number on success

## 测试用例

### 1. Append event to 存储

Should append event和return a new event_id和sequence_number=1.

输入：

```json
{"src":"service","dest":"eventstore","body":{"type":"append","msg_id":1,"aggregate_id":"user-123","event_type":"UserCreated","event_data":{"name":"John"},"version":0}}
```

期望输出：

```text
{"type": "appended", "in_reply_to": 1, "event_id": ".*", "sequence_number": 1}
```

### 2. Detect concurrent modification

Version mismatch should return a concurrency_error.

输入：

```json
{"src":"service","dest":"eventstore","body":{"type":"append","msg_id":1,"aggregate_id":"user-123","event_type":"UserUpdated","event_data":{"name":"Jane"},"version":5}}
```

期望输出：

```text
{"type": "concurrency_error", "in_reply_to": 1, "error": "Expected version 5, got 0"}
```

## 参考资料

- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)：Martin Fowler's introduction to event sourcing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
