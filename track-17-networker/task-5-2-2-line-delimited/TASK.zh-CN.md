# 实现行分隔分帧（Redis RESP 风格）

英文标题：Implement Line-Delimited Framing (Redis RESP Style)
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-2-line-delimited>

课程：17. 网络器：TCP 与协议基础
任务序号：7
短标题：行分隔分帧
难度：进阶
子主题：消息分帧与序列化

## 中文导读

这道题让你实现另一种常见的消息分帧方式：行分隔（Line-Delimited）。不同于长度前缀方案，这种方式用特殊字符 `\r\n` 来标记一条消息的结束，Redis 的 RESP 协议、HTTP/1.1 的请求头以及 SMTP 协议都采用了这种方式。核心难点在于 TCP 不保证一次读取就能拿到完整的一行，`\r\n` 甚至可能被拆分到两次读取中，所以你必须正确地缓冲和拼接数据。

## 题目说明

实现行分隔分帧，每条消息以 `\r\n` 结尾。这种方式被 Redis RESP 协议、HTTP/1.1 请求头和 SMTP 协议所采用。

核心挑战在于：TCP 不保证一次读取就能拿到完整的一行数据。你必须正确处理部分读取的情况，使用缓冲区来拼接数据。

实现以下消息处理器：

```json
Request:  {"type": "line_encode", "msg_id": 1, "message": "PING"}
Response: {"type": "line_encode_ok", "in_reply_to": 1, "encoded": "PING\r\n", "bytes": 6}

Request:  {"type": "line_decode", "msg_id": 2, "buffer": "PING\r\nPONG\r\n"}
Response: {"type": "line_decode_ok", "in_reply_to": 2, "messages": ["PING", "PONG"], "remaining": ""}

Request:  {"type": "line_decode", "msg_id": 3, "buffer": "PING\r\nPON"}
Response: {"type": "line_decode_ok", "in_reply_to": 3, "messages": ["PING"], "remaining": "PON"}
```

## 涉及概念

- `line-delimited`
- `RESP protocol`
- `CRLF`
- `partial reads`
- `buffer management`

## 实现提示

- 消息以 \r\n（回车换行，即 CRLF）作为终止符
- 持续缓冲收到的字节，直到找到完整的 \r\n
- 需要处理 \r\n 被拆分到两次 TCP 读取中的情况
- 这与 Redis RESP 协议的工作方式类似
- 对于超过最大长度限制的消息应返回错误

## 测试用例

### 1. 编码一条行消息

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

### 2. 解码多条完整的行

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

- [Redis Serialization Protocol (RESP)](https://redis.io/docs/reference/protocol-spec/)：Redis 协议规范，采用 CRLF 行分隔的分帧方式

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
