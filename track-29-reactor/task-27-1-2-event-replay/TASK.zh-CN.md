# 实现 Event Replay

英文标题：Implement Event Replay
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-2-event-replay>

课程：29. 反应器：事件溯源与 CQRS
任务序号：2
短标题：Event Replay
难度：intermediate
子主题：Event Sourcing

## 中文导读

本题要求你完成 `实现 Event Replay`。

重点关注：`event replay`、`state reconstruction`、`snapshot-based replay`、`temporal query`、`fold over events`。

建议先按提示逐步实现：Replay applies each event in sequence order to rebuild state from scratch。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Event replay rebuilds an aggregate's state by applying all of its stored events in order. It is the core read mechanism in event sourcing: state is never stored directly, only derived by replaying history.

Implement a 节点 that supports three replay modes:

```JSON
// Full replay: apply all events to get current state
{ "type": "replay", "msg_id": 1, "aggregate_id": "user-123" }
-> { "type": "replayed", "in_reply_to": 1,
    "aggregate_id": "user-123",
    "events_replayed": 5, "state": {"name": "Jane"} }

// Snapshot-based replay: load snapshot, apply only events after its version
{ "type": "replay", "msg_id": 2,
  "aggregate_id": "user-123", "use_snapshot": true }
-> { "type": "replayed", "in_reply_to": 2,
    "aggregate_id": "user-123",
    "snapshot_version": 100, "events_replayed": 2 }

// Temporal query: replay only events up to the given timestamp
{ "type": "get_state", "msg_id": 3,
  "aggregate_id": "user-123", "timestamp": "2024-01-15T09:00:00Z" }
-> { "type": "state", "in_reply_to": 3,
    "aggregate_id": "user-123",
    "timestamp": "2024-01-15T09:00:00Z",
    "state": {"name": "John Doe"} }
```

For snapshot-based replay, `events_replayed` counts only events applied after the snapshot version. Temporal queries ignore any event recorded after the requested timestamp.

## 涉及概念

- `event replay`
- `state reconstruction`
- `snapshot-based replay`
- `temporal query`
- `fold over events`

## 实现提示

- Replay applies each event in sequence order to rebuild state from scratch
- With a snapshot, start from the saved state和only replay events after that version
- A temporal query replays only events，包含timestamp <= the target time
- Merge each event_data dict into the running state dict on every replay step
- snapshot_version in the 响应 is the version at which the snapshot was taken

## 测试用例

### 1. Replay events to rebuild state

Should replay all events和return final state.

输入：

```json
{"src":"replayer","dest":"eventstore","body":{"type":"replay","msg_id":1,"aggregate_id":"user-123"}}
```

期望输出：

```text
{"type": "replayed", "in_reply_to": 1, "aggregate_id": "user-123", "events_replayed": 5, "state": {"name": "Jane"}}
```

### 2. Replay from snapshot

Should start from snapshot和replay only newer events.

输入：

```json
{"src":"replayer","dest":"eventstore","body":{"type":"replay","msg_id":1,"aggregate_id":"user-123","use_snapshot":true}}
```

期望输出：

```text
{"type": "replayed", "in_reply_to": 1, "aggregate_id": "user-123", "snapshot_version": 100, "events_replayed": 2}
```

## 参考资料

- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)：Martin Fowler's introduction to event sourcing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
