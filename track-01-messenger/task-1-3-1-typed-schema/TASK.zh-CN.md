#模式l 消息格式，包含类型化模式

英文标题：Model Message格式，包含Typed Schema
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-1-typed-schema>

课程：1. 信使：消息通信基础
任务序号：11
短标题：类型化模式
难度：intermediate
子主题：The Protocol Beneath

## 中文导读

本题要求你完成 `Model 消息格式，包含类型化模式`。

重点关注：`serialization`、`deserialization`、`schema design`、`type safety`。

建议先按提示逐步实现：Define a 消息 class，包含src, dest,和body fields。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Raw JSON is just strings. A typed schema wraps the raw 消息 in classes，包含explicit fields, validation,和serialization methods — making it impossible to accidentally send a malformed 消息.

Implement a `消息` class，包含`to_json()` / `from_json()` methods和a `MessageBody` class. Your 节点 handles `init`, `echo`,和a new `validate` 消息 type:

```JSON
{ "type": "validate", "msg_id": 1,
  "payload": "{\"src\":\"a\",\"dest\":\"b\",\"body\":{\"type\":\"x\"}}" }
-> { "type": "validate_ok", "in_reply_to": 1,
    "valid": true, "fields": ["src", "dest", "body.type"] }
```

The `validate` handler parses the JSON string in `payload`和reports which top-level和nested fields are present. If the payload is not valid JSON, return `valid: false`，包含an empty `fields` list.

## 涉及概念

- `serialization`
- `deserialization`
- `schema design`
- `type safety`

## 实现提示

- Define a 消息 class，包含src, dest,和body fields
- Body should have type, msg_id,和in_reply_to fields at minimum
- Implement to_json()和from_json() methods用于serialization
- Validate field types during deserialization
-处理missing optional fields，包含sensible defaults

## 测试用例

### 1. 初始化和回声，包含类型化模式

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"typed"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "typed", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Validate a well-formed payload

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"validate","msg_id":2,"payload":"{\"src\":\"a\",\"dest\":\"b\",\"body\":{\"type\":\"x\"}}"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "validate_ok", "valid": true, "fields": ["src", "dest", "body.type"], "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Protocol Buffers Overview](https://protobuf.dev/overview/)：How Google defines typed 消息 schemas用于分布式系统

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
