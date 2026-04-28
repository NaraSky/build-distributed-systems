# 实现 Protocol Evolution

英文标题：Implement Protocol Evolution
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-4-protocol-evolution>

课程：27. 迁移器：数据与协议演进
任务序号：9
短标题：Protocol Evolution
难度：advanced
子主题：Protocol和API Evolution

## 中文导读

本题要求你完成 `实现 Protocol Evolution`。

重点关注：`Protocol Buffers`、`backward compatibility`、`unknown field handling`、`version negotiation`、`message transformation`。

建议先按提示逐步实现：Protocol Buffers: unknown fields from a newer schema are ignored by older readers。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

As services evolve, they add new fields和change 消息 schemas. Protocol evolution strategies ensure old services can still read new 消息 (by ignoring unknown fields)和new services can still serve old clients (by transforming 消息 down to old schemas).

Implement a 节点 that handles protocol encoding, decoding, negotiation,和transformation:

```JSON
// Encode a 消息，包含Protocol Buffers
{ "type": "encode", "msg_id": 1, "format": "protobuf",
  "data": {"id":1,"email":"user@example.com","full_name":"John Doe"} }
-> { "type": "encoded", "in_reply_to": 1,
    "format": "protobuf", "encoded": "<base64>",
    "fields": ["id","email","full_name"] }

// Old schema decodes v2 消息: unknown fields are silently dropped
{ "type": "decode", "msg_id": 2, "format": "protobuf",
  "schema": "v1", "data": "<base64-v2>" }
-> { "type": "decoded", "in_reply_to": 2,
    "schema": "v1",
    "data": {"id":1,"email":"user@example.com"},
    "unknown_fields_ignored": true }

// Negotiate highest common version
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

- Protocol Buffers: unknown fields from a newer schema are ignored by older readers
- Decode，包含old schema: ignore fields the old schema does not know about
- Protocol negotiation: choose the highest version that both 客户端和服务端 support
- Transform v2->v1: map new field names back to old names (full_name -> name)
- Encoding returns the field names actually serialised into the 消息

## 测试用例

### 1. Protocol Buffers backward compatibility

Should encode all three fields和return base64 representation.

输入：

```json
{"src":"client_v1","dest":"service","body":{"type":"encode","msg_id":1,"format":"protobuf","data":{"id":1,"email":"user@example.com","full_name":"John Doe"}}}
```

期望输出：

```text
{"type": "encoded", "in_reply_to": 1, "format": "protobuf", "encoded": ".*", "fields": ["id", "email", "full_name"]}
```

### 2. Decode，包含old schema (ignores unknown fields)

Old v1 schema should decode v2 消息和silently drop full_name.

输入：

```json
{"src":"service","dest":"decoder","body":{"type":"decode","msg_id":1,"format":"protobuf","schema":"v1","data":"BASE64_ENCODED_V2"}}
```

期望输出：

```text
{"type": "decoded", "in_reply_to": 1, "schema": "v1", "data": {"id": 1, "email": "user@example.com"}, "unknown_fields_ignored": true}
```

## 参考资料

- [Protocol Buffers](https://protobuf.dev/)：Protocol Buffers: language-neutral, extensible serialization format
- [API Protocol Evolution](https://www.connolly.tech/p/api-protocol-evolution/)：API Protocol Evolution guide

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
