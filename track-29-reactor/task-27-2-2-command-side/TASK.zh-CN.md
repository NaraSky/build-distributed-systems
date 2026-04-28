# 实现 Command Side 校验和Execution

英文标题：Implement Command Side Validation和Execution
网页：<https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-2-command-side>

课程：29. 反应器：事件溯源与 CQRS
任务序号：7
短标题：Command Side
难度：intermediate
子主题：CQRS (Command Query Responsibility Segregation)

## 中文导读

本题要求你完成 `实现 Command Side 校验和Execution`。

重点关注：`command validation`、`business rules`、`command handler`、`domain events`、`invariant enforcement`。

建议先按提示逐步实现：Schema validation: check required fields和types before business rules。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The command side is the write path in CQRS. Before any state change is applied, the command must pass two layers of validation: **schema validation** (correct fields和types)和**business rule validation** (domain constraints). Only then is the command executed和a domain event emitted.

Implement a 节点 that processes commands through both validation layers:

```JSON
// Schema error: missing required field
{ "type": "CreateUser", "msg_id": 1,
  "payload": {"name": "John"} }      // email missing
-> { "type": "validation_failed", "in_reply_to": 1,
    "valid": false, "errors": ["Email is required"] }

// Business rule error: age constraint
{ "type": "CreateUser", "msg_id": 2,
  "payload": {"name": "John", "email": "j@example.com", "age": 16} }
-> { "type": "validation_failed", "in_reply_to": 2,
    "valid": false, "errors": ["User must be 18 or older"] }

// All validation passes: execute和emit domain event
{ "type": "CreateUser", "msg_id": 3,
  "payload": {"name": "John", "email": "j@example.com", "age": 25} }
-> { "type": "command_executed", "in_reply_to": 3,
    "success": true,
    "events": [{"type": "UserCreated", "payload": {"id": "<uuid>"}}] }
```

When multiple validations fail, collect all errors和return them together. Never execute the command if any validation fails.

## 涉及概念

- `command validation`
- `business rules`
- `command handler`
- `domain events`
- `invariant enforcement`

## 实现提示

- Schema validation: check required fields和types before business rules
- Business rule validation: enforce domain constraints (age >= 18, unique email, etc.)
- Return all validation errors together, not just the first one
- Only call the command handler after all validation passes
- Emit a domain event (UserCreated) that describes what happened, not what was requested

## 测试用例

### 1. Validate command format

Missing email should fail schema validation.

输入：

```json
{"src":"client","dest":"commandside","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John"}}}
```

期望输出：

```text
{"type": "validation_failed", "in_reply_to": 1, "valid": false, "errors": ["Email is required"]}
```

### 2. Validate business rules

Age under 18 should fail business rule validation.

输入：

```json
{"src":"client","dest":"commandside","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John","email":"john@example.com","age":16}}}
```

期望输出：

```text
{"type": "validation_failed", "in_reply_to": 1, "valid": false, "errors": ["User must be 18 or older"]}
```

## 参考资料

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)：CQRS和the command side design

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
