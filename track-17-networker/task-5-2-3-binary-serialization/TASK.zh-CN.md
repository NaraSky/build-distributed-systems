# 实现 a Binary Serialization格式

英文标题：Implement a Binary Serialization格式
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-3-binary-serialization>

课程：17. 网络器：TCP 与协议基础
任务序号：8
短标题：Binary Serialization
难度：advanced
子主题：消息 Framing和Serialization

## 中文导读

本题要求你完成 `实现 a Binary Serialization格式`。

重点关注：`binary serialization`、`MessagePack`、`type tags`、`compact encoding`。

建议先按提示逐步实现：Use a type tag byte before each value: 0x01=int, 0x02=string, 0x03=array, 0x04=map。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a binary serialization format (similar to MessagePack). Support four types: integers, strings, arrays,和maps. Compare size和performance to JSON.

Type tags:
- `0x01`: integer (4 bytes big-endian)
- `0x02`: string (2-byte length + UTF-8 bytes)
- `0x03`: array (2-byte count + N encoded values)
- `0x04`: map (2-byte count + N key-value pairs)

Implement handlers:

```JSON
请求:  {"type": "bin_encode", "msg_id": 1, "value": {"name": "Alice", "age": 30}}
响应: {"type": "bin_encode_ok", "in_reply_to": 1, "encoded_hex": "...", "size_bytes": 20, "json_size_bytes": 27, "savings_pct": 25.9}

请求:  {"type": "bin_decode", "msg_id": 2, "encoded_hex": "..."}
响应: {"type": "bin_decode_ok", "in_reply_to": 2, "value": {"name": "Alice", "age": 30}}

请求:  {"type": "bin_benchmark", "msg_id": 3, "payload_sizes": [100, 1000, 10000]}
响应: {"type": "bin_benchmark_ok", "in_reply_to": 3, "results": [
    {"size": 100, "json_bytes": 100, "binary_bytes": 72, "ratio": 0.72}
]}
```

## 涉及概念

- `binary serialization`
- `MessagePack`
- `type tags`
- `compact encoding`

## 实现提示

- Use a type tag byte before each value: 0x01=int, 0x02=string, 0x03=array, 0x04=map
- Integers use a fixed 4-byte big-endian encoding
- Strings are prefixed，包含a 2-byte length followed by UTF-8 bytes
- Arrays are prefixed，包含a 2-byte count, followed by that many encoded values
- Compare the encoded size to JSON用于the same data

## 测试用例

### 1. Encode a simple integer

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bin_encode","msg_id":2,"value":42}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bin_encode_ok", "in_reply_to": 2, "encoded_hex": "010000002a", "size_bytes": 5, "msg_id": 1}}
```

### 2. Encode和decode roundtrip

Encode should produce hex用于string "hello". Decode of that hex should return "hello".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bin_encode","msg_id":2,"value":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"bin_decode","msg_id":3,"encoded_hex":"02000568656c6c6f"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [MessagePack Specification](https://msgpack.org/)：MessagePack: an efficient binary serialization format

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
