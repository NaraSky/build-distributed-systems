# 实现 Request/Response Transformation

英文标题：Implement Request/Response Transformation
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-3-transformation>

课程：12. 代理
任务序号：8
短标题：Request/Response Transformation
难度：intermediate
子主题：API Gateway

## 中文导读

本题要求你完成 `实现 Request/Response Transformation`。

重点关注：`request transformation`、`response transformation`、`protocol translation`、`format conversion`、`legacy integration`。

建议先按提示逐步实现：Transform 请求 format before sending to backend (e.g., JSON → XML)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

API gateways transform requests和responses to bridge the gap between 客户端 expectations和backend implementations. This enables legacy integration和protocol translation.

**Transformation types**:
```
1.格式 transformation:
   客户端 (JSON) → Gateway → Backend (XML)

2. Protocol translation:
   客户端 (REST) → Gateway → Backend (gRPC)

3. Field mapping:
   客户端 (userId) → Gateway → Backend (user_id)

4. Aggregation:
   客户端 → Gateway → [Backend A, Backend B] → Gateway → 客户端
```

**Example: JSON to XML transformation**:
```JSON
// 客户端 sends JSON:
请求:  {"type": "api_request", "msg_id": 1, "method": "POST", "path": "/api/users", "headers": {"Content-Type": "application/JSON"}, "body": {"name": "Alice", "email": "alice@example.com"}}

// Gateway transforms to XML和sends to backend:
Backend 请求:  {"method": "POST", "path": "/users", "headers": {"Content-Type": "application/xml"}, "body": "<?xml version="1.0"?><user><name>Alice</name><email>alice@example.com</email></user>"}

// Backend responds，包含XML:
Backend 响应:  {"status": 201, "body": "<?xml version="1.0"?><user><id>123</id><name>Alice</name><email>alice@example.com</email></user>"}

// Gateway transforms to JSON和sends to 客户端:
响应: {"type": "api_response", "in_reply_to": 1, "status": 201, "body": {"id": 123, "name": "Alice", "email": "alice@example.com"}}
```

**Field mapping configuration**:
```JSON
{
  "transformations": {
    "/api/users": {
      "请求": {
        "field_mappings": {
          "userId": "user_id",
          "firstName": "first_name",
          "lastName": "last_name"
        },
        "format": "json_to_xml"
      },
      "响应": {
        "field_mappings": {
          "user_id": "userId",
          "first_name": "firstName",
          "last_name": "lastName"
        },
        "format": "xml_to_json"
      }
    }
  }
}
```

## 涉及概念

- `request transformation`
- `response transformation`
- `protocol translation`
- `format conversion`
- `legacy integration`

## 实现提示

- Transform 请求 format before sending to backend (e.g., JSON → XML)
- Transform 响应 format before returning to 客户端 (e.g., XML → JSON)
- Protocol translation: REST → gRPC, GraphQL → REST
- Legacy integration: modern JSON clients → legacy XML backends
- Field mapping: rename fields between 客户端和backend schemas

## 测试用例

### 1. JSON to XML transformation

Gateway should transform JSON 请求 to XML before sending to backend.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"transformations":{"/api/users":{"request":{"format":"json_to_xml"},"response":{"format":"xml_to_json"}}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"POST","path":"/api/users","body":{"name":"Alice"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Field mapping

Gateway should map userId→user_id in 请求, user_id→userId in 响应.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"POST","path":"/api/users","body":{"userId":"user123","firstName":"Alice"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "body": {"userId": "user123", "firstName": "Alice"}}}
```

## 参考资料

- [API Gateway Transformation](https://aws.amazon.com/api-gateway/)：AWS API Gateway documentation on 请求/响应 transformation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
