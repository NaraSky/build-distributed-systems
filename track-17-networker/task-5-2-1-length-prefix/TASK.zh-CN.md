# 实现 Length-Prefixed 消息 Framing

英文标题：Implement Length-Prefixed Message Framing
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-1-length-prefix>

课程：17. 网络器：TCP 与协议基础
任务序号：6
短标题：Length-Prefix Framing
难度：intermediate
子主题：消息 Framing和Serialization

## 中文导读

本题要求你完成 `实现 Length-Prefixed 消息 Framing`。

重点关注：`message framing`、`length prefix`、`TCP stream`、`partial reads`。

建议先按提示逐步实现：Each 消息 is [4-byte big-endian length][payload]。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

TCP is a byte stream, not a 消息 protocol. You need framing to know where one 消息 ends和the next begins. Length-prefixed framing prepends each 消息，包含its size.

Format: `[4-byte big-endian length][payload]`

Implement `send_frame`和`recv_frame`:

```JSON
请求:  {"type": "frame_encode", "msg_id": 1, "payload": "hello world"}
响应: {"type": "frame_encode_ok", "in_reply_to": 1, "frame_hex": "0000000b68656c6c6f20776f726c64", "total_bytes": 15}

请求:  {"type": "frame_decode", "msg_id": 2, "frame_hex": "0000000b68656c6c6f20776f726c64"}
响应: {"type": "frame_decode_ok", "in_reply_to": 2, "payload": "hello world", "payload_length": 11}

请求:  {"type": "frame_decode_partial", "msg_id": 3, "chunks": ["0000000b68", "656c6c6f20", "776f726c64"]}
响应: {"type": "frame_decode_partial_ok", "in_reply_to": 3, "payload": "hello world", "chunks_needed": 3}
```

## 涉及概念

- `message framing`
- `length prefix`
- `TCP stream`
- `partial reads`

## 实现提示

- Each 消息 is [4-byte big-endian length][payload]
- The receiver must read exactly 4 bytes first to get the length
- Then read exactly length bytes用于the payload
- TCP does not guarantee 消息 boundaries; handle partial reads
- Use a buffer to accumulate bytes until a full frame is available

## 测试用例

### 1. Encode a simple 消息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"frame_encode","msg_id":2,"payload":"hello"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "frame_encode_ok", "in_reply_to": 2, "frame_hex": "0000000568656c6c6f", "total_bytes": 9, "msg_id": 1}}
```

### 2. Decode a framed 消息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"frame_decode","msg_id":2,"frame_hex":"0000000568656c6c6f"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "frame_decode_ok", "in_reply_to": 2, "payload": "hello", "payload_length": 5, "msg_id": 1}}
```

## 参考资料

- [Message Framing in TCP](https://blog.stephencleary.com/2009/04/message-framing.html)：Comprehensive overview of different 消息 framing strategies用于TCP

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
