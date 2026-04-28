# 实现命令查询职责分离与事件溯源的集成

英文标题：Implement CQRS with Event Sourcing
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-5-cqrs-event-sourcing>

课程：29. 反应器：事件溯源与 CQRS
任务序号：10
短标题：CQRS + 事件溯源
难度：高级
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你将命令查询职责分离和事件溯源两大模式端到端地集成起来。这是本课程的综合实战：命令通过写入端存入事件存储（作为唯一的事实来源），事件再驱动投影构建，查询端从投影中读取数据。这样既保留了事件溯源的完整审计日志，又获得了读写分离带来的高效读取性能。

## 题目说明

命令查询职责分离和事件溯源（Event Sourcing）天生就是一对搭档：命令写入事件存储（作为唯一的事实来源），从事件构建的投影则服务于查询。这样你既拥有事件溯源提供的完整操作历史，又享有读写分离带来的高效读取性能。

你需要实现一个端到端集成这两种模式的节点：

```json
// 命令：校验 -> 应用到聚合体 -> 持久化事件 -> 更新投影
{ "type": "command", "msg_id": 1,
  "command": {"type": "CreateUser",
               "payload": {"id": "user-123", "name": "John"}} }
-> { "type": "command_result", "in_reply_to": 1,
    "success": true,
    "events": [{"eventType": "UserCreated", "aggregateId": "user-123"}] }

// 查询：从投影中读取（绝不直接从事件存储读取）
{ "type": "query", "msg_id": 2,
  "query": {"type": "GetUser", "params": {"userId": "user-123"}} }
-> { "type": "query_result", "in_reply_to": 2,
    "data": {"id": "user-123", "name": "John"} }

// 时间点查询：回放事件存储到某个时间点
{ "type": "query", "msg_id": 3,
  "query": {"type": "GetUserAtTime",
             "params": {"userId": "user-123",
                        "timestamp": "2024-01-15T09:00:00Z"}} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": {"id": "user-123", "name": "John Doe",
             "at_time": "2024-01-15T09:00:00Z"} }
```

命令的处理流程是：校验参数 -> 应用到聚合体 -> 追加事件到事件存储 -> 更新投影。查询的处理流程是：从投影中读取（获取当前状态）或回放事件存储（获取历史状态）。

## 概念说明

事件溯源就像一本详细的账本：不记录"账户余额是多少"，而是记录每一笔"存了 100 元""取了 50 元"的操作。任何时候想知道余额，把账本从头到尾加一遍就行。想知道上个月月底的余额？从头加到上个月最后一笔就行。投影就像一个"余额看板"，它根据账本实时更新，查询的人直接看看板就好，不用每次都翻账本。聚合体（Aggregate）就是那个"账户"本身，它负责校验每笔操作是否合法（比如不能取超过余额的钱）。

## 涉及概念

- `CQRS`
- `event sourcing`
- `aggregate`
- `projection`
- `temporal query`
- `full-stack integration`

## 实现提示

- 命令经过校验后应用到聚合体上，聚合体产生事件
- 事件被存储到事件存储中，然后应用到投影上
- 查询从投影中读取，而不是直接从事件存储中读取
- 时间点查询通过回放事件存储到指定时间戳来实现
- 每次执行命令时，聚合体版本号必须与预期版本号匹配（乐观锁机制）

## 测试用例

### 1. 通过事件溯源执行命令

命令应产生一个包含正确聚合体标识的 UserCreated 事件。

输入：

```json
{"src":"client","dest":"cqrs","body":{"type":"command","msg_id":1,"command":{"type":"CreateUser","payload":{"id":"user-123","name":"John"}}}}
```

期望输出：

```text
{"type": "command_result", "in_reply_to": 1, "success": true, "events": [{"eventType": "UserCreated", "aggregateId": "user-123"}]}
```

### 2. 从投影中查询

查询应从投影中读取数据，而不是从事件存储中读取。

输入：

```json
{"src":"client","dest":"cqrs","body":{"type":"query","msg_id":1,"query":{"type":"GetUser","params":{"userId":"user-123"}}}}
```

期望输出：

```text
{"type": "query_result", "in_reply_to": 1, "data": {"id": "user-123", "name": "John"}}
```

## 参考资料

- [CQRS and Event Sourcing](https://martinfowler.com/bliki/CQRS.html)：将命令查询职责分离与事件溯源相结合，实现完整的审计能力和高效的读取性能

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
