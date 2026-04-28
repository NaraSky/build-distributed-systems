# 实现协议演进

英文标题：Implement Protocol Evolution
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-4-protocol-evolution>

课程：27. 迁移器：数据与协议演进
任务序号：9
短标题：Protocol Evolution
难度：高级
子主题：Protocol and API Evolution

## 中文导读

这道题要求你实现一个处理协议编码、解码、版本协商和消息转换的节点。随着服务的演进，消息格式会不断变化。协议演进（Protocol Evolution）策略确保旧服务仍能读取新消息（忽略不认识的字段），新服务也能服务旧客户端（将消息转换为旧格式）。这是微服务架构中保持系统长期可演进的核心技术。

## 题目说明

随着服务的演进，它们会添加新字段并修改消息模式。协议演进策略确保旧服务仍能读取新消息（通过忽略未知字段），新服务也能服务旧客户端（通过将消息转换为旧模式）。

请实现一个处理协议编码、解码、协商和转换的节点：

```json
// 使用 Protocol Buffers 编码消息
{ "type": "encode", "msg_id": 1, "format": "protobuf",
  "data": {"id":1,"email":"user@example.com","full_name":"John Doe"} }
-> { "type": "encoded", "in_reply_to": 1,
    "format": "protobuf", "encoded": "<base64>",
    "fields": ["id","email","full_name"] }

// 旧模式解码 v2 消息：未知字段被静默丢弃
{ "type": "decode", "msg_id": 2, "format": "protobuf",
  "schema": "v1", "data": "<base64-v2>" }
-> { "type": "decoded", "in_reply_to": 2,
    "schema": "v1",
    "data": {"id":1,"email":"user@example.com"},
    "unknown_fields_ignored": true }

// 协商双方都支持的最高版本
{ "type": "negotiate", "msg_id": 3,
  "client_versions": ["1.0","2.0"] }
-> { "type": "negotiated", "in_reply_to": 3,
    "version": "2.0",
    "server_versions": ["1.0","2.0","3.0"] }
```

## 涉及概念

- `Protocol Buffers`
- `backward compatibility`
- `unknown field handling`
- `version negotiation`
- `message transformation`

## 实现提示

- Protocol Buffers 的特性：旧版读取器会忽略来自新模式的未知字段
- 使用旧模式解码时：忽略旧模式不认识的字段
- 协议协商：选择客户端和服务端都支持的最高版本
- v2 转 v1：将新字段名映射回旧字段名（例如 full_name 映射为 name）
- 编码操作返回实际序列化到消息中的字段名列表

## 测试用例

### 1. Protocol Buffers 向后兼容

应编码所有三个字段并返回 base64 表示。

输入：

```json
{"src":"client_v1","dest":"service","body":{"type":"encode","msg_id":1,"format":"protobuf","data":{"id":1,"email":"user@example.com","full_name":"John Doe"}}}
```

期望输出：

```text
{"type": "encoded", "in_reply_to": 1, "format": "protobuf", "encoded": ".*", "fields": ["id", "email", "full_name"]}
```

### 2. 使用旧模式解码（忽略未知字段）

旧的 v1 模式应能解码 v2 消息，并静默丢弃 full_name 字段。

输入：

```json
{"src":"service","dest":"decoder","body":{"type":"decode","msg_id":1,"format":"protobuf","schema":"v1","data":"BASE64_ENCODED_V2"}}
```

期望输出：

```text
{"type": "decoded", "in_reply_to": 1, "schema": "v1", "data": {"id": 1, "email": "user@example.com"}, "unknown_fields_ignored": true}
```

## 参考资料

- [Protocol Buffers](https://protobuf.dev/)：语言无关、可扩展的序列化格式
- [API Protocol Evolution](https://www.connolly.tech/p/api-protocol-evolution/)：API 协议演进指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
