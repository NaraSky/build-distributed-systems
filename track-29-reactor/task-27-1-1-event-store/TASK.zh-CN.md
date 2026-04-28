# 实现事件存储

英文标题：Implement Event Store
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-1-event-store>

课程：29. 反应器：事件溯源与 CQRS
任务序号：1
短标题：事件存储
难度：进阶
子主题：Event Sourcing

## 中文导读

本题要求你实现一个事件存储（Event Store）节点。事件存储是事件溯源架构的核心组件，它像一本只能追加、不能涂改的日记本，把每一次数据变更都记录为不可变的事件。掌握它是理解事件溯源的第一步，也是后续事件回放、投影等高级功能的基础。

## 题目说明

事件存储（Event Store）是一个**仅追加日志（Append-Only Log）**，每个聚合体（Aggregate）的所有变更都以不可变的事件形式记录在其中。要获取当前状态，你需要按顺序回放所有事件，或者从快照（Snapshot）开始回放。已写入的状态绝不允许被覆盖。

你需要实现一个节点，为多个聚合体管理事件，并支持**乐观并发控制（Optimistic Concurrency Control）**：调用者需要声明它期望的版本号；如果另一个写入者已经修改了该聚合体，追加操作将被拒绝。

```json
// 追加一个事件（version 必须匹配当前聚合体的版本号）
{ "type": "append", "msg_id": 1,
  "aggregate_id": "user-123", "event_type": "UserCreated",
  "event_data": {"name": "John"}, "version": 0 }
-> { "type": "appended", "in_reply_to": 1,
    "event_id": "<uuid>", "sequence_number": 1 }

// 版本号不匹配 -> 拒绝
{ "type": "append", "version": 5 }   // 实际版本号是 0
-> { "type": "concurrency_error", "in_reply_to": 1,
    "error": "Expected version 5, got 0" }

// 在聚合体的当前版本保存一个快照
{ "type": "create_snapshot", "msg_id": 3, "aggregate_id": "user-123" }
-> { "type": "snapshot_created", "in_reply_to": 3,
    "aggregate_id": "user-123", "version": 1 }
```

每个聚合体的版本号从 0 开始。每次成功追加事件，聚合体的版本号加 1，全局序列号（Sequence Number）也随之递增。

## 概念说明

事件溯源（Event Sourcing）的核心思想是：不存储"最终结果"，而是存储"每一步变化"。打个比方，传统数据库像是只记录银行账户余额，而事件存储则记录了每一笔存取款记录。你随时可以从头回放这些记录，算出当前余额。

乐观并发控制就像这样一个场景：两个人同时想编辑同一篇文章，系统用版本号来检测冲突。如果你在版本 3 的基础上修改，但提交时发现文章已经变成了版本 4，系统就会拒绝你的修改，让你重新读取最新版本后再试。

## 涉及概念

- `event sourcing`
- `append-only log`
- `optimistic concurrency`
- `aggregate`
- `sequence number`
- `snapshot`

## 实现提示

- 事件是不可变的，只能追加，不能修改或删除
- 为每个聚合体维护一个版本号；如果请求中的版本号与当前版本号不匹配，拒绝追加
- 序列号是全局的，跨所有聚合体单调递增
- 快照存储聚合体在某个特定版本的状态，用于加速回放
- 成功时返回一个自动生成的事件标识和新的序列号

## 测试用例

### 1. 向事件存储中追加事件

应追加事件并返回新生成的事件标识和序列号（序列号为 1）。

输入：

```json
{"src":"service","dest":"eventstore","body":{"type":"append","msg_id":1,"aggregate_id":"user-123","event_type":"UserCreated","event_data":{"name":"John"},"version":0}}
```

期望输出：

```text
{"type": "appended", "in_reply_to": 1, "event_id": ".*", "sequence_number": 1}
```

### 2. 检测并发修改冲突

版本号不匹配时应返回并发错误。

输入：

```json
{"src":"service","dest":"eventstore","body":{"type":"append","msg_id":1,"aggregate_id":"user-123","event_type":"UserUpdated","event_data":{"name":"Jane"},"version":5}}
```

期望输出：

```text
{"type": "concurrency_error", "in_reply_to": 1, "error": "Expected version 5, got 0"}
```

## 参考资料

- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)：Martin Fowler 对事件溯源的入门介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
