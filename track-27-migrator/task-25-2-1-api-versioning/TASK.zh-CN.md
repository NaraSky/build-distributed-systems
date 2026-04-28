# 实现 API Versioning

英文标题：Implement API Versioning
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-1-api-versioning>

课程：27. 迁移器：数据与协议演进
任务序号：6
短标题：API Versioning
难度：intermediate
子主题：Protocol和API Evolution

## 中文导读

本题要求你完成 `实现 API Versioning`。

重点关注：`API versioning`、`URL versioning`、`deprecation headers`、`content negotiation`、`sunset`。

建议先按提示逐步实现：Route requests by version field or Accept header to the correct handler。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

API versioning lets you evolve your API without breaking existing clients. You support multiple versions simultaneously, warn clients on deprecated ones，包含`Deprecation`和`Sunset` headers,和eventually stop serving a version after its sunset date，包含HTTP 410.

Implement a 节点 that routes和manages API versions:

```JSON
// Route to the correct version handler
{ "type": "get_users", "msg_id": 1, "version": "v2" }
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v2",
    "users": [{"id":1,"email":"user@example.com","full_name":"John Doe"}] }

// Deprecated version: add warning headers
{ "type": "get_users", "msg_id": 2, "version": "v1", "deprecated": true }
-> { "type": "users_response", "in_reply_to": 2,
    "version": "v1",
    "headers": {"Deprecation":"true","Sunset":"2024-12-31"} }

// Version negotiation via Accept header
{ "type": "get_users", "msg_id": 3 }
headers: { "Accept": "application/vnd.myapi.v2+JSON" }
-> { "type": "users_response", "in_reply_to": 3,
    "version": "v2", "content_type": "application/vnd.myapi.v2+JSON" }

// Sunset version returns 410 Gone
{ "type": "get_users", "msg_id": 4, "version": "v1", "sunset": true }
-> { "type": "error", "in_reply_to": 4, "status": 410,
    "error": "API version v1.0 has been sunset",
    "current_version": "v2.0" }
```

## 涉及概念

- `API versioning`
- `URL versioning`
- `deprecation headers`
- `content negotiation`
- `sunset`

## 实现提示

- Route requests by version field or Accept header to the correct handler
- Deprecation header: Deprecation: true plus Sunset: <date> on v1 responses
- Content negotiation: parse version from Accept: application/vnd.myapi.v2+JSON
- Sunset (410 Gone): once the sunset date passes, reject requests，包含HTTP 410
- Never remove a version without a sunset date announced in advance

## 测试用例

### 1. Route to correct API version

Should route to v2 handler which returns full_name field.

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"version":"v2"}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "version": "v2", "users": [{"id": 1, "email": "user@example.com", "full_name": "John Doe"}]}
```

### 2. Deprecation headers

Deprecated version should include Deprecation和Sunset headers.

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"version":"v1","deprecated":true}}
```

期望输出：

```text
{"type": "users_response", "in_reply_to": 1, "version": "v1", "headers": {"Deprecation": "true", "Sunset": "2024-12-31"}}
```

## 参考资料

- [API Versioning Strategies](https://restfulapi.net/versioning/)：URL versioning, header versioning,和media type versioning compared
- [Semantic Versioning](https://semver.org/)：Semantic Versioning specification

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
