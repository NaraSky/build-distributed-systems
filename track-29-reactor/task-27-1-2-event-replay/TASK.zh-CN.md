# 实现事件回放

英文标题：Implement Event Replay
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-2-event-replay>

课程：29. 反应器：事件溯源与 CQRS
任务序号：2
短标题：事件回放
难度：进阶
子主题：Event Sourcing

## 中文导读

本题要求你实现事件回放（Event Replay）功能。在事件溯源中，系统不直接存储状态，而是通过按顺序重放所有历史事件来"还原"出当前状态。这就像看一盘棋的录像，从第一步走到最后一步，就能知道当前棋盘的局面。理解事件回放是掌握事件溯源读取机制的关键。

## 题目说明

事件回放通过按顺序应用聚合体（Aggregate）的所有已存储事件来重建其状态。这是事件溯源的核心读取机制：状态从不直接存储，而是通过回放历史事件推导得出。

你需要实现一个支持三种回放模式的节点：

```json
// 完整回放：应用所有事件得到当前状态
{ "type": "replay", "msg_id": 1, "aggregate_id": "user-123" }
-> { "type": "replayed", "in_reply_to": 1,
    "aggregate_id": "user-123",
    "events_replayed": 5, "state": {"name": "Jane"} }

// 基于快照的回放：加载快照，只应用快照版本之后的事件
{ "type": "replay", "msg_id": 2,
  "aggregate_id": "user-123", "use_snapshot": true }
-> { "type": "replayed", "in_reply_to": 2,
    "aggregate_id": "user-123",
    "snapshot_version": 100, "events_replayed": 2 }

// 时间点查询：只回放给定时间戳之前的事件
{ "type": "get_state", "msg_id": 3,
  "aggregate_id": "user-123", "timestamp": "2024-01-15T09:00:00Z" }
-> { "type": "state", "in_reply_to": 3,
    "aggregate_id": "user-123",
    "timestamp": "2024-01-15T09:00:00Z",
    "state": {"name": "John Doe"} }
```

使用基于快照的回放时，`events_replayed` 只统计快照版本之后实际应用的事件数量。时间点查询会忽略请求时间戳之后的所有事件。

## 涉及概念

- `event replay`
- `state reconstruction`
- `snapshot-based replay`
- `temporal query`
- `fold over events`

## 实现提示

- 回放是按序列号顺序逐个应用事件，从零开始重建状态
- 使用快照时，从快照保存的状态开始，只回放该版本之后的事件
- 时间点查询只回放时间戳小于等于目标时间的事件
- 每个回放步骤都将事件数据合并到当前运行状态中
- 响应中的快照版本号是快照被创建时对应的版本号

## 测试用例

### 1. 回放事件重建状态

应回放所有事件并返回最终状态。

输入：

```json
{"src":"replayer","dest":"eventstore","body":{"type":"replay","msg_id":1,"aggregate_id":"user-123"}}
```

期望输出：

```text
{"type": "replayed", "in_reply_to": 1, "aggregate_id": "user-123", "events_replayed": 5, "state": {"name": "Jane"}}
```

### 2. 从快照回放

应从快照开始，只回放快照之后的新事件。

输入：

```json
{"src":"replayer","dest":"eventstore","body":{"type":"replay","msg_id":1,"aggregate_id":"user-123","use_snapshot":true}}
```

期望输出：

```text
{"type": "replayed", "in_reply_to": 1, "aggregate_id": "user-123", "snapshot_version": 100, "events_replayed": 2}
```

## 参考资料

- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)：Martin Fowler 对事件溯源的入门介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
