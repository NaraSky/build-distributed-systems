# 实现 Protocol Versioning，包含Backward Compatibility

英文标题：Implement Protocol Versioning，包含Backward Compatibility
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-5-protocol-versioning>

课程：17. 网络器：TCP 与协议基础
任务序号：10
短标题：Protocol Versioning
难度：intermediate
子主题：消息 Framing和Serialization

## 中文导读

本题要求你完成 `实现 Protocol Versioning，包含Backward Compatibility`。

重点关注：`protocol versioning`、`backward compatibility`、`wire format`、`migration`。

建议先按提示逐步实现：Include a protocol_version field in the 消息 header。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a protocol versioning scheme. The sender includes a `protocol_version` in the header. The receiver handles backward compatibility用于older versions.

Protocol versions:
- **v1**: `{version: 1, key: string, value: string}`
- **v2**: `{version: 2, key: string, value: string|int, timestamp_ms: number, tags: string[]}`

When receiving a v1 消息, upgrade it to v2，包含defaults: `timestamp_ms = 0`, `tags = []`.

Implement handlers:

```JSON
请求:  {"type": "proto_send_v1", "msg_id": 1, "key": "name", "value": "Alice"}
响应: {"type": "proto_send_v1_ok", "in_reply_to": 1, "wire_version": 1}

请求:  {"type": "proto_send_v2", "msg_id": 2, "key": "age", "value": 30, "timestamp_ms": 1700000000, "tags": ["user"]}
响应: {"type": "proto_send_v2_ok", "in_reply_to": 2, "wire_version": 2}

请求:  {"type": "proto_receive", "msg_id": 3, "wire_version": 1, "key": "name", "value": "Alice"}
响应: {"type": "proto_receive_ok", "in_reply_to": 3, "parsed_version": 2, "key": "name", "value": "Alice", "timestamp_ms": 0, "tags": []}
```

## 涉及概念

- `protocol versioning`
- `backward compatibility`
- `wire format`
- `migration`

## 实现提示

- Include a protocol_version field in the 消息 header
- Version 1: basic key-value，包含string values only
- Version 2: adds integer values和a timestamp field
- The receiver must handle both v1和v2 消息
- Use sensible defaults用于missing fields when upgrading v1 to v2

## 测试用例

### 1. Send v1 消息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"proto_send_v1","msg_id":2,"key":"name","value":"Alice"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "proto_send_v1_ok", "in_reply_to": 2, "wire_version": 1, "msg_id": 1}}
```

### 2. Receive v1 消息 upgraded to v2

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"proto_receive","msg_id":2,"wire_version":1,"key":"name","value":"Alice"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "proto_receive_ok", "in_reply_to": 2, "parsed_version": 2, "key": "name", "value": "Alice", "timestamp_ms": 0, "tags": [], "msg_id": 1}}
```

## 参考资料

- [Protocol Buffers - Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/)：How Protocol Buffers handle schema evolution和backward compatibility

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
