# 实现事件驱动的读取模型更新

英文标题：Implement Event-Driven Read Model Updates
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-4-event-driven-updates>

课程：29. 反应器：事件溯源与 CQRS
任务序号：9
短标题：事件驱动更新
难度：进阶
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你实现事件驱动的读取模型更新机制。在 CQRS 架构中，命令端产生事件，查询端必须监听这些事件来保持读取模型的同步。这个"监听并更新"的组件叫做投影器。它需要处理两个关键问题：一是订阅感兴趣的事件类型，二是保证幂等性，即同一个事件被重复投递时不会重复处理。

## 题目说明

在 CQRS 中，命令端产生事件，查询端必须对这些事件做出响应，以保持读取模型的实时更新。**事件驱动的投影器（Projector）** 订阅事件总线，每当相关事件到达时就更新一个或多个读取模型。

你需要实现一个具备订阅和幂等更新能力的投影器节点：

```json
// 注册对特定事件类型的订阅
{ "type": "subscribe", "msg_id": 1,
  "event_types": ["UserCreated", "UserUpdated"] }
-> { "type": "subscribed", "in_reply_to": 1,
    "event_types": ["UserCreated", "UserUpdated"] }

// 事件到达：更新所有相关的读取模型
{ "type": "event", "msg_id": 2,
  "event": {"type": "UserCreated",
             "payload": {"id": "user-123", "name": "John"}} }
-> { "type": "read_models_updated", "in_reply_to": 2,
    "event_id": "evt-123",
    "updated_models": ["user_listing", "user_by_email"] }

// 相同的事件再次到达：跳过处理
{ "type": "event", "msg_id": 3,
  "event": {"type": "UserCreated", "id": "evt-123",
             "payload": {"id": "user-123"}} }
-> { "type": "event_skipped", "in_reply_to": 3,
    "event_id": "evt-123", "reason": "already_processed" }
```

幂等性至关重要：事件总线可能多次投递同一个事件。在应用任何更新之前，务必先检查事件标识。

## 概念说明

想象投影器就像一个新闻编辑：它订阅了特定类型的新闻源（事件类型），每收到一条新闻就更新对应的专栏（读取模型）。但如果同一条新闻被重复投递了，编辑不会傻傻地发两遍，而是识别出这是重复的直接跳过。这就是幂等性的含义。

## 涉及概念

- `event bus`
- `projector`
- `subscription`
- `idempotent updates`
- `eventual consistency`

## 实现提示

- 订阅操作注册投影器，使其能从事件总线接收指定类型的事件
- 当事件到达时，更新所有关注该事件类型的读取模型
- 记录已处理的事件标识；对重复事件返回跳过响应（保证幂等性）
- updated_models 列出所有实际被更新的读取模型名称
- 最终一致性：读取模型可能会比写入模型略有延迟

## 测试用例

### 1. 订阅事件

应确认成功订阅了两种事件类型。

输入：

```json
{"src":"projector","dest":"eventbus","body":{"type":"subscribe","msg_id":1,"event_types":["UserCreated","UserUpdated"]}}
```

期望输出：

```text
{"type": "subscribed", "in_reply_to": 1, "event_types": ["UserCreated", "UserUpdated"]}
```

### 2. 收到事件后更新读取模型

UserCreated 事件应同时更新 user_listing 和 user_by_email 两个读取模型。

输入：

```json
{"src":"eventbus","dest":"projector","body":{"type":"event","msg_id":1,"event":{"type":"UserCreated","payload":{"id":"user-123","name":"John"}}}}
```

期望输出：

```text
{"type": "read_models_updated", "in_reply_to": 1, "event_id": "evt-123", "updated_models": ["user_listing", "user_by_email"]}
```

## 参考资料

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)：CQRS 中事件驱动的读取模型更新

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
