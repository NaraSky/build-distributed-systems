# 实现协议版本管理与向后兼容

英文标题：Implement Protocol Versioning with Backward Compatibility
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-5-protocol-versioning>

课程：17. 网络器：TCP 与协议基础
任务序号：10
短标题：协议版本管理
难度：进阶
子主题：消息分帧与序列化

## 中文导读

这道题让你实现协议的版本管理方案。在真实的分布式系统中，协议不可能一成不变，总会随着业务需求不断演进。问题在于：新版本上线后，旧版本的客户端还没来得及升级怎么办？向后兼容（Backward Compatibility）就是解决这个问题的关键。你需要让接收方能同时处理新旧两个版本的消息，收到旧版本消息时自动填入合理的默认值将其升级为新版本。

## 题目说明

实现一套协议版本管理方案。发送方在消息头中携带 `protocol_version`，接收方负责处理旧版本的向后兼容。

协议版本定义：
- **v1**：`{version: 1, key: string, value: string}`
- **v2**：`{version: 2, key: string, value: string|int, timestamp_ms: number, tags: string[]}`

当收到 v1 消息时，自动升级为 v2 格式，使用默认值：`timestamp_ms = 0`，`tags = []`。

实现以下消息处理器：

```json
Request:  {"type": "proto_send_v1", "msg_id": 1, "key": "name", "value": "Alice"}
Response: {"type": "proto_send_v1_ok", "in_reply_to": 1, "wire_version": 1}

Request:  {"type": "proto_send_v2", "msg_id": 2, "key": "age", "value": 30, "timestamp_ms": 1700000000, "tags": ["user"]}
Response: {"type": "proto_send_v2_ok", "in_reply_to": 2, "wire_version": 2}

Request:  {"type": "proto_receive", "msg_id": 3, "wire_version": 1, "key": "name", "value": "Alice"}
Response: {"type": "proto_receive_ok", "in_reply_to": 3, "parsed_version": 2, "key": "name", "value": "Alice", "timestamp_ms": 0, "tags": []}
```

## 涉及概念

- `protocol versioning`
- `backward compatibility`
- `wire format`
- `migration`

## 实现提示

- 在消息头中包含 protocol_version 字段
- 版本 1：基础的键值对，值只支持字符串类型
- 版本 2：新增了整数值支持和时间戳字段
- 接收方必须同时处理 v1 和 v2 两种消息
- 当将 v1 升级为 v2 时，为缺失的字段使用合理的默认值

## 测试用例

### 1. 发送 v1 消息

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

### 2. 接收 v1 消息并升级为 v2

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

- [Protocol Buffers - Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/)：Protocol Buffers 如何处理模式演进和向后兼容

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
