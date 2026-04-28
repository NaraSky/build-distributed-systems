# Define和Encode Protocol Buffer Messages

英文标题：Define和Encode Protocol Buffer Messages
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-1-protobuf-schema>

课程：17. 网络器：TCP 与协议基础
任务序号：11
短标题：Protobuf Schema
难度：intermediate
子主题：gRPC和Protocol Buffers

## 中文导读

本题要求你完成 `Define和Encode Protocol Buffer Messages`。

重点关注：`Protocol Buffers`、`schema definition`、`field numbering`、`varint encoding`。

建议先按提示逐步实现：Protobuf uses field numbers instead of field names on the wire。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Protocol Buffers use a schema definition (.proto file)和a compact binary wire format. Each field has a number, type,和wire encoding.

Wire format: each field is `(field_number << 3 | wire_type)` followed by the value.

Implement a protobuf encoder/decoder用于a simple 消息:

```proto
消息 Person {
    string name = 1;
    int32 age = 2;
    string email = 3;
}
```

Implement handlers:

```JSON
请求:  {"type": "proto_define", "msg_id": 1, "schema": {"name": "Person", "fields": [
    {"name": "name", "number": 1, "type": "string"},
    {"name": "age", "number": 2, "type": "int32"},
    {"name": "email", "number": 3, "type": "string"}
]}}
响应: {"type": "proto_define_ok", "in_reply_to": 1, "message_name": "Person", "field_count": 3}

请求:  {"type": "proto_encode", "msg_id": 2, "消息": "Person", "data": {"name": "Alice", "age": 30, "email": "alice@example.com"}}
响应: {"type": "proto_encode_ok", "in_reply_to": 2, "encoded_hex": "...", "size_bytes": 28}
```

## 涉及概念

- `Protocol Buffers`
- `schema definition`
- `field numbering`
- `varint encoding`

## 实现提示

- Protobuf uses field numbers instead of field names on the wire
- Varint encoding uses 7 bits per byte，包含MSB continuation flag
- Wire types: 0=varint, 1=64-bit, 2=length-delimited, 5=32-bit
- Each field is encoded as (field_number << 3 | wire_type)
- String fields use wire type 2: tag + length + bytes

## 测试用例

### 1. Define a protobuf schema

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"proto_define","msg_id":2,"schema":{"name":"Person","fields":[{"name":"name","number":1,"type":"string"},{"name":"age","number":2,"type":"int32"}]}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "proto_define_ok", "in_reply_to": 2, "message_name": "Person", "field_count": 2, "msg_id": 1}}
```

### 2. Encode a protobuf 消息

proto_encode_ok should contain valid protobuf hex encoding. Name field: tag 0x0a then length then ASCII. Age field: tag 0x10 then varint 30.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"proto_define","msg_id":2,"schema":{"name":"Person","fields":[{"name":"name","number":1,"type":"string"},{"name":"age","number":2,"type":"int32"}]}}}
{"src":"c1","dest":"n1","body":{"type":"proto_encode","msg_id":3,"message":"Person","data":{"name":"Alice","age":30}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Protocol Buffers Encoding](https://protobuf.dev/programming-guides/encoding/)：How Protocol Buffers encode data on the wire (varint, length-delimited, etc.)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
