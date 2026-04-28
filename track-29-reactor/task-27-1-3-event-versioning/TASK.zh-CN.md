# 实现 Event Versioning和Migration

英文标题：Implement Event Versioning和Migration
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-3-event-versioning>

课程：29. 反应器：事件溯源与 CQRS
任务序号：3
短标题：Event Versioning
难度：advanced
子主题：Event Sourcing

## 中文导读

本题要求你完成 `实现 Event Versioning和Migration`。

重点关注：`event versioning`、`schema evolution`、`upcasting`、`backward compatibility`、`migration`。

建议先按提示逐步实现：Upcasting transforms an old event version to the target version in-place。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Event schemas change over time as requirements evolve. A field gets added, renamed, or split. Because old events are immutable, you cannot change them in place — instead you **upcast** them: transform older versions to the current schema on read.

Implement a 节点 that handles event schema migration through upcasting:

```JSON
// Upcast a single event from v1 to v2
// v1 UserCreated has: id, name
// v2 UserCreated adds: email (default "")
{ "type": "upcast", "msg_id": 1,
  "event": {"event_type": "UserCreated", "version": 1,
            "event_data": {"id": 1, "name": "John"}},
  "target_version": 2 }
-> { "type": "upcasted", "in_reply_to": 1,
    "event": {"event_type": "UserCreated", "version": 2,
              "event_data": {"id": 1, "name": "John", "email": ""}} }

// Migrate a batch of events to the target version
{ "type": "migrate_batch", "msg_id": 2,
  "events": [
    {"event_type": "UserCreated", "version": 1, "event_data": {"id": 1}}
  ],
  "target_version": 2 }
-> { "type": "migrated", "in_reply_to": 2,
    "count": 1, "target_version": 2 }
```

Your upcaster must handle multi-step migration (e.g. v1 -> v2 -> v3) by chaining single-version upgrades. Each step adds or defaults the fields introduced in that version.

## 涉及概念

- `event versioning`
- `schema evolution`
- `upcasting`
- `backward compatibility`
- `migration`

## 实现提示

- Upcasting transforms an old event version to the target version in-place
- When upcasting from v1 to v2, fill missing fields，包含sensible defaults (empty string, 0, etc.)
- migrate_batch iterates over the events array和upcasts each one
- count in the migrate_batch 响应 is the total number of events processed
- Events already at the target version should be returned unchanged

## 测试用例

### 1. Upcast event to new version

Should add missing email field，包含default empty string when upcasting v1->v2.

输入：

```json
{"src":"migrator","dest":"eventstore","body":{"type":"upcast","msg_id":1,"event":{"event_type":"UserCreated","version":1,"event_data":{"id":1,"name":"John"}},"target_version":2}}
```

期望输出：

```text
{"type": "upcasted", "in_reply_to": 1, "event": {"event_type": "UserCreated", "version": 2, "event_data": {"id": 1, "name": "John", "email": ""}}}
```

### 2. Migrate batch of events

Should migrate all events和return count.

输入：

```json
{"src":"migrator","dest":"eventstore","body":{"type":"migrate_batch","msg_id":1,"events":[{"event_type":"UserCreated","version":1,"event_data":{"id":1}}],"target_version":2}}
```

期望输出：

```text
{"type": "migrated", "in_reply_to": 1, "count": 1, "target_version": 2}
```

## 参考资料

- [Event Versioning Patterns](https://leanpub.com/esversioning/read)：Greg Young's guide to versioning events in event-sourced systems

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
