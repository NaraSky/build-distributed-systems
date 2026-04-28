# 实现 CQRS Fundamentals

英文标题：Implement CQRS Fundamentals
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-1-cqrs-fundamentals>

课程：29. 反应器：事件溯源与 CQRS
任务序号：6
短标题：CQRS Fundamentals
难度：intermediate
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你完成 `实现 CQRS Fundamentals`。

重点关注：`CQRS`、`command bus`、`query bus`、`command validation`、`read model`。

建议先按提示逐步实现：Commands change state和emit events; queries only read和never mutate。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

CQRS (Command Query Responsibility Segregation) separates every operation into either a **command** (write, changes state) or a **query** (read, never changes state). Commands和queries are handled by separate buses，包含separate models, enabling each side to be optimised independently.

Implement a 节点 that routes 消息 to the correct bus:

```JSON
// Command: validate payload, apply change, return emitted events
{ "type": "CreateUser", "msg_id": 1,
  "payload": {"name": "John", "email": "john@example.com"} }
-> { "type": "command_result", "in_reply_to": 1,
    "success": true,
    "events": [{"type": "UserCreated", "payload": {"id": "<uuid>", "name": "John"}}] }

// Command validation 故障
{ "type": "CreateUser", "msg_id": 2,
  "payload": {"name": "John"} }    // missing email
-> { "type": "command_result", "in_reply_to": 2,
    "success": false,
    "errors": ["Email is required"] }

// Query: read from read model, no state change
{ "type": "GetUser", "msg_id": 3,
  "params": {"user_id": "user-123"} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": {"id": "user-123", "name": "John Doe"} }
```

The key rule: if the operation changes state, it is a command; if it only reads, it is a query. A single operation must never do both.

## 涉及概念

- `CQRS`
- `command bus`
- `query bus`
- `command validation`
- `read model`
- `write model separation`

## 实现提示

- Commands change state和emit events; queries only read和never mutate
- A command handler validates the payload, applies the change,和returns the emitted events
- A query handler reads from a pre-built read model和returns data
- Validation 故障 should return success=false，包含an errors array
- Route by the 消息 type field: CreateUser goes to command bus, GetUser to query bus

## 测试用例

### 1.处理command

Valid command should succeed和return emitted events.

输入：

```json
{"src":"client","dest":"commandbus","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John","email":"john@example.com"}}}
```

期望输出：

```text
{"type": "command_result", "in_reply_to": 1, "success": true, "events": [{"type": "UserCreated", "payload": {"id": ".*", "name": "John"}}]}
```

### 2. Execute query

Query should return data from read model without changing state.

输入：

```json
{"src":"client","dest":"querybus","body":{"type":"GetUser","msg_id":1,"params":{"user_id":"user-123"}}}
```

期望输出：

```text
{"type": "query_result", "in_reply_to": 1, "data": {"id": "user-123", "name": "John Doe"}}
```

## 参考资料

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)：Martin Fowler's explanation of Command Query Responsibility Segregation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
