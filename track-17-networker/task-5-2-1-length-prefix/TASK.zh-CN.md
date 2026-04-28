# 实现长度前缀消息分帧

英文标题：Implement Length-Prefixed Message Framing
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-1-length-prefix>

课程：17. 网络器：TCP 与协议基础
任务序号：6
短标题：长度前缀分帧
难度：进阶
子主题：消息分帧与序列化

## 中文导读

这道题让你解决 TCP 编程中一个最基本的问题：消息边界。TCP 是一个字节流协议，它不会告诉你"一条消息到哪里结束"。就像往水管里倒水，接收方拿到的只是一段连续的字节流。长度前缀分帧（Length-Prefixed Framing）是最常用的解决方案之一：在每条消息前面加上 4 个字节表示消息长度，这样接收方就能精确知道该读多少字节来还原完整的消息。

## 题目说明

TCP 是一个字节流协议，而不是消息协议。你需要通过分帧（Framing）来确定一条消息在哪里结束、下一条消息从哪里开始。长度前缀分帧的做法是在每条消息前面加上它的大小。

格式：`[4 字节大端序长度][消息体]`

实现 `send_frame` 和 `recv_frame`：

```json
Request:  {"type": "frame_encode", "msg_id": 1, "payload": "hello world"}
Response: {"type": "frame_encode_ok", "in_reply_to": 1, "frame_hex": "0000000b68656c6c6f20776f726c64", "total_bytes": 15}

Request:  {"type": "frame_decode", "msg_id": 2, "frame_hex": "0000000b68656c6c6f20776f726c64"}
Response: {"type": "frame_decode_ok", "in_reply_to": 2, "payload": "hello world", "payload_length": 11}

Request:  {"type": "frame_decode_partial", "msg_id": 3, "chunks": ["0000000b68", "656c6c6f20", "776f726c64"]}
Response: {"type": "frame_decode_partial_ok", "in_reply_to": 3, "payload": "hello world", "chunks_needed": 3}
```

## 涉及概念

- `message framing`
- `length prefix`
- `TCP stream`
- `partial reads`

## 实现提示

- 每条消息的格式为：[4 字节大端序长度][消息体]
- 接收方必须先精确读取 4 个字节以获取消息长度
- 然后再精确读取指定长度的字节作为消息体
- TCP 不保证消息边界，需要处理分多次读取的情况（部分读取）
- 使用缓冲区累积字节，直到收集到一个完整的帧

## 测试用例

### 1. 编码一条简单消息

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

### 2. 解码一条分帧消息

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

- [Message Framing in TCP](https://blog.stephencleary.com/2009/04/message-framing.html)：全面介绍 TCP 中不同消息分帧策略的文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
