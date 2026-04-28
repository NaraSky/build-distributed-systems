# 实现 Line-Delimited Framing (Redis RESP Style)

英文标题：Implement Line-Delimited Framing (Redis RESP Style)
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-2-line-delimited>

课程：17. 网络器：TCP 与协议基础
任务序号：7
短标题：Line-Delimited Framing
难度：intermediate
子主题：消息 Framing和Serialization

## 中文导读

本题要求你完成 `实现 Line-Delimited Framing (Redis RESP Style)`。

重点关注：`line-delimited`、`RESP protocol`、`CRLF`、`partial reads`、`buffer management`。

建议先按提示逐步实现：消息 are terminated by \r\n (CRLF)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement line-delimited framing where 消息 end，包含`\r\n`. This is the approach used by Redis RESP, HTTP/1.1 headers,和SMTP.

The challenge: TCP doesn't guarantee that a full line arrives in one read. You must buffer partial reads correctly.

Implement handlers:

```JSON
请求:  {"type": "line_encode", "msg_id": 1, "消息": "PING"}
响应: {"type": "line_encode_ok", "in_reply_to": 1, "encoded": "PING\r\n", "bytes": 6}

请求:  {"type": "line_decode", "msg_id": 2, "buffer": "PING\r\nPONG\r\n"}
响应: {"type": "line_decode_ok", "in_reply_to": 2, "消息": ["PING", "PONG"], "remaining": ""}

请求:  {"type": "line_decode", "msg_id": 3, "buffer": "PING\r\nPON"}
响应: {"type": "line_decode_ok", "in_reply_to": 3, "消息": ["PING"], "remaining": "PON"}
```

## 涉及概念

- `line-delimited`
- `RESP protocol`
- `CRLF`
- `partial reads`
- `buffer management`

## 实现提示

- 消息 are terminated by \r\n (CRLF)
- Buffer incoming bytes until you find a complete \r\n
-处理the case where \r\n is split across two TCP reads
- This is similar to how Redis RESP protocol works
- Return an error用于消息 that exceed a maximum length limit

## 测试用例

### 1. Encode a line 消息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"line_encode","msg_id":2,"message":"PING"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "line_encode_ok", "in_reply_to": 2, "encoded": "PING\r\n", "bytes": 6, "msg_id": 1}}
```

### 2. Decode multiple complete lines

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"line_decode","msg_id":2,"buffer":"GET key1\r\nSET key2 val\r\n"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "line_decode_ok", "in_reply_to": 2, "messages": ["GET key1", "SET key2 val"], "remaining": "", "msg_id": 1}}
```

## 参考资料

- [Redis Serialization Protocol (RESP)](https://redis.io/docs/reference/protocol-spec/)：Redis protocol specification使用CRLF-delimited framing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
