# 实现请求与响应转换

英文标题：Implement Request/Response Transformation
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-3-transformation>

课程：12. 代理
任务序号：8
短标题：请求/响应转换
难度：进阶
子主题：API 网关

## 中文导读

这道题要求你在 API 网关中实现请求和响应的格式转换功能。在实际系统中，客户端和后端服务可能使用不同的数据格式或协议。例如，客户端使用 JSON，而老旧的后端系统只接受 XML。网关可以在中间进行格式转换，让双方无需做任何修改就能正常通信。

## 题目说明

API 网关通过转换请求和响应来弥合客户端期望与后端实现之间的差异。这使得遗留系统集成和协议转换成为可能。

**转换类型**：
```
1. 格式转换：
   客户端 (JSON) → 网关 → 后端 (XML)

2. 协议转换：
   客户端 (REST) → 网关 → 后端 (gRPC)

3. 字段映射：
   客户端 (userId) → 网关 → 后端 (user_id)

4. 聚合：
   客户端 → 网关 → [后端 A, 后端 B] → 网关 → 客户端
```

**示例：JSON 转 XML**：
```json
// 客户端发送 JSON：
Request:  {"type": "api_request", "msg_id": 1, "method": "POST", "path": "/api/users", "headers": {"Content-Type": "application/json"}, "body": {"name": "Alice", "email": "alice@example.com"}}

// 网关将 JSON 转为 XML 后发送给后端：
Backend Request:  {"method": "POST", "path": "/users", "headers": {"Content-Type": "application/xml"}, "body": "<?xml version=\"1.0\"?><user><name>Alice</name><email>alice@example.com</email></user>"}

// 后端返回 XML 响应：
Backend Response:  {"status": 201, "body": "<?xml version=\"1.0\"?><user><id>123</id><name>Alice</name><email>alice@example.com</email></user>"}

// 网关将 XML 转为 JSON 后返回给客户端：
Response: {"type": "api_response", "in_reply_to": 1, "status": 201, "body": {"id": 123, "name": "Alice", "email": "alice@example.com"}}
```

**字段映射配置**：
```json
{
  "transformations": {
    "/api/users": {
      "request": {
        "field_mappings": {
          "userId": "user_id",
          "firstName": "first_name",
          "lastName": "last_name"
        },
        "format": "json_to_xml"
      },
      "response": {
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

- 在发送给后端之前转换请求格式（例如 JSON 转 XML）
- 在返回给客户端之前转换响应格式（例如 XML 转 JSON）
- 协议转换：REST 转 gRPC、GraphQL 转 REST
- 遗留系统集成：让使用 JSON 的现代客户端能够与使用 XML 的老旧后端通信
- 字段映射：在客户端和后端的数据模型之间进行字段名重命名

## 测试用例

### 1. JSON 转 XML

网关应在将请求发送给后端之前，将 JSON 格式转换为 XML 格式。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"transformations":{"/api/users":{"request":{"format":"json_to_xml"},"response":{"format":"xml_to_json"}}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"POST","path":"/api/users","body":{"name":"Alice"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 字段映射

网关应在请求中将 userId 映射为 user_id，在响应中将 user_id 映射回 userId。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"POST","path":"/api/users","body":{"userId":"user123","firstName":"Alice"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "body": {"userId": "user123", "firstName": "Alice"}}}
```

## 参考资料

- [API Gateway Transformation](https://aws.amazon.com/api-gateway/)：AWS API Gateway 关于请求/响应转换的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
