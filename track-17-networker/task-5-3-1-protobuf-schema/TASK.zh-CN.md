# 定义和编码 Protocol Buffer 消息

英文标题：Define and Encode Protocol Buffer Messages
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-1-protobuf-schema>

课程：17. 网络器：TCP 与协议基础
任务序号：11
短标题：Protobuf 模式定义
难度：进阶
子主题：gRPC 与 Protocol Buffers

## 中文导读

这道题让你深入 Protocol Buffers（简称 Protobuf）的底层编码原理。Protobuf 是 Google 开源的一种高效序列化框架，它通过 .proto 文件定义数据结构，然后用紧凑的二进制格式在网络上传输。与 JSON 不同，Protobuf 在传输时不带字段名，而是用字段编号来标识，大大减小了数据体积。通过亲手实现 Protobuf 的编码器和解码器，你将理解变长整数编码（Varint）、线路类型等核心概念。

## 题目说明

Protocol Buffers 使用模式定义文件（.proto 文件）和紧凑的二进制线路格式。每个字段都有一个编号、一个类型和对应的线路编码方式。

线路格式：每个字段编码为 `(field_number << 3 | wire_type)` 加上字段值。

为一个简单的消息实现 Protobuf 编码器/解码器：

```proto
message Person {
    string name = 1;
    int32 age = 2;
    string email = 3;
}
```

实现以下消息处理器：

```json
Request:  {"type": "proto_define", "msg_id": 1, "schema": {"name": "Person", "fields": [
    {"name": "name", "number": 1, "type": "string"},
    {"name": "age", "number": 2, "type": "int32"},
    {"name": "email", "number": 3, "type": "string"}
]}}
Response: {"type": "proto_define_ok", "in_reply_to": 1, "message_name": "Person", "field_count": 3}

Request:  {"type": "proto_encode", "msg_id": 2, "message": "Person", "data": {"name": "Alice", "age": 30, "email": "alice@example.com"}}
Response: {"type": "proto_encode_ok", "in_reply_to": 2, "encoded_hex": "...", "size_bytes": 28}
```

## 涉及概念

- `Protocol Buffers`
- `schema definition`
- `field numbering`
- `varint encoding`

## 实现提示

- Protobuf 在线路上使用字段编号而非字段名，从而节省空间
- 变长整数编码（Varint）每个字节使用 7 位存储数据，最高位作为是否还有后续字节的标志
- 线路类型：0 表示变长整数，1 表示 64 位定长，2 表示长度分隔，5 表示 32 位定长
- 每个字段编码为 (field_number << 3 | wire_type)
- 字符串字段使用线路类型 2：标签 + 长度 + 字节内容

## 测试用例

### 1. 定义 Protobuf 模式

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

### 2. 编码 Protobuf 消息

验证说明：proto_encode_ok 应包含合法的 Protobuf 十六进制编码。name 字段：标签 0x0a 后跟长度再跟 ASCII 字节。age 字段：标签 0x10 后跟变长整数 30。

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

- [Protocol Buffers Encoding](https://protobuf.dev/programming-guides/encoding/)：详解 Protocol Buffers 如何在线路上编码数据（变长整数、长度分隔等）

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
