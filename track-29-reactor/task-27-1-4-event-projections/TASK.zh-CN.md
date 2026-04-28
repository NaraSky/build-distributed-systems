# 实现事件投影

英文标题：Implement Event Projections
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-4-event-projections>

课程：29. 反应器：事件溯源与 CQRS
任务序号：4
短标题：事件投影
难度：进阶
子主题：Event Sourcing

## 中文导读

本题要求你实现事件投影（Projection）功能。事件存储天然适合写入，但不方便查询。投影就像一个"专题摘要"：它监听事件流，把事件转化为方便查询的读取模型。当需求变了或者需要新的查询视图时，还可以从头重建投影。这是连接事件溯源写入端和查询端的关键桥梁。

## 题目说明

事件存储针对写入做了优化，但并不适合直接查询。**投影（Projection）** 解决了这个问题：它监听事件流，维护一个反范式化的读取模型（Read Model），让查询变得高效。当事件结构发生变化或者需要一个新的查询视图时，可以从头重建投影。

你需要实现一个管理命名投影的节点：

```json
// 创建一个初始状态为空的新投影
{ "type": "create", "msg_id": 1,
  "name": "user-listing", "initial_state": [] }
-> { "type": "projection_created", "in_reply_to": 1,
    "name": "user-listing", "version": 0 }

// 将一个事件应用到投影上
{ "type": "update", "msg_id": 2,
  "projection": "user-listing",
  "event": {"event_type": "UserCreated",
             "event_data": {"id": "user-123", "name": "John"}} }
-> { "type": "projection_updated", "in_reply_to": 2,
    "projection": "user-listing", "version": 1,
    "state": [{"id": "user-123", "name": "John"}] }

// 使用一组历史事件从头重建投影
{ "type": "rebuild", "msg_id": 3,
  "projection": "user-listing",
  "events": [{"event_type": "UserCreated", "event_data": {"id": "user-123"}}] }
-> { "type": "projection_rebuilt", "in_reply_to": 3,
    "projection": "user-listing",
    "events_processed": 1, "version": 1 }
```

投影的版本号在每次应用事件时加 1。重建操作会将版本号重置为 0，然后重放所有提供的事件。

## 涉及概念

- `projections`
- `read models`
- `event-driven denormalization`
- `rebuild`
- `versioned projection`

## 实现提示

- 投影是一个命名的读取模型，通过逐条消费事件来构建
- 创建操作初始化一个空状态、版本号为 0 的投影
- 更新操作将一个事件应用到投影上，并递增版本号
- 重建操作从头开始，将一组事件重新应用到投影上
- 每次更新或重建步骤都应将事件数据合并到投影状态中

## 测试用例

### 1. 创建列表投影

应创建一个版本号为 0 的新投影。

输入：

```json
{"src":"projector","dest":"projection","body":{"type":"create","msg_id":1,"name":"user-listing","initial_state":[]}}
```

期望输出：

```text
{"type": "projection_created", "in_reply_to": 1, "name": "user-listing", "version": 0}
```

### 2. 通过事件更新投影

应将用户添加到列表中，并将版本号递增到 1。

输入：

```json
{"src":"eventstore","dest":"projection","body":{"type":"update","msg_id":1,"projection":"user-listing","event":{"event_type":"UserCreated","event_data":{"id":"user-123","name":"John"}}}}
```

期望输出：

```text
{"type": "projection_updated", "in_reply_to": 1, "projection": "user-listing", "version": 1, "state": [{"id": "user-123", "name": "John"}]}
```

## 参考资料

- [Projections in Event Sourcing](https://eventstore.com/blog/projections/)：介绍投影如何将事件转化为查询优化的读取模型

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
