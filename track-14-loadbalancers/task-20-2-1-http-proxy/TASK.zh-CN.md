# 实现七层 HTTP 代理

英文标题：Implement Layer 7 HTTP Proxy
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-1-http-proxy>

课程：14. 负载均衡器
任务序号：6
短标题：HTTP 代理
难度：进阶
子主题：七层负载均衡

## 中文导读

本题要求你实现一个七层 HTTP 代理。它就像一个聪明的"中间人"，能读懂客户端发来的 HTTP 请求内容（比如访问的路径、请求头等），然后根据预设的规则把请求转发给合适的后端服务器。这是构建现代微服务网关和反向代理（如 Nginx、Envoy）的基础能力。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

七层负载均衡工作在 HTTP 应用层，通过检查请求头和 URL 路径来做出路由决策。与四层（TCP）不同，七层代理能理解 HTTP 语义。

**HTTP 代理架构**：
```
Client → L7 Proxy → Backend
  - Parse HTTP request
  - Inspect headers (Host, User-Agent, Cookies)
  - Inspect URL path (/api/users, /static/images)
  - Select backend based on rules
  - Forward request and return response
```

**请求流程**：
```
1. Client sends: GET /api/users HTTP/1.1
   Host: example.com

2. Proxy parses:
   - Method: GET
   - Path: /api/users
   - Host: example.com

3. Proxy routes to backend pool "api"

4. Backend responds: HTTP/1.1 200 OK
   {"users": [...]}

5. Proxy returns response to client
```

**请求示例**：
```json
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "headers": {"Host": "example.com", "User-Agent": "Mozilla"}}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"Content-Type": "application/json"}, "body": "{"users": [{"id": 1, "name": "Alice"}]}", "backend": "api-1"}
```

**后端池配置**：
```json
{
  "backend_pools": {
    "api": {
      "backends": ["api-1:8080", "api-2:8080", "api-3:8080"],
      "algorithm": "round-robin"
    },
    "static": {
      "backends": ["static-1:8080", "static-2:8080"],
      "algorithm": "least-connections"
    }
  }
}
```

## 涉及概念

- `layer 7 load balancing`
- `HTTP proxy`
- `request routing`
- `header inspection`
- `backend selection`

## 实现提示

- 解析传入的 HTTP 请求，提取 Host 请求头和 URL 路径
- 维护一个后端池，并跟踪各后端的健康状态
- 根据路由规则选择一个后端
- 将请求转发到后端，并将响应返回给客户端
- 处理连接池和长连接

## 测试用例

### 1. 将 HTTP GET 请求路由到正确的后端

响应应返回状态码 200，并指明是哪个后端处理了该请求（例如 api-1）。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","headers":{"Host":"example.com"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1"}}
```

### 2. 根据 URL 路径路由

发往 /static/* 的请求应该路由到静态资源后端池。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/static/logo.png","headers":{"Host":"example.com"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "static-1"}}
```

## 参考资料

- [Layer 7 Load Balancing](https://www.nginx.com/resources/glossary/layer-7-load-balancing/)：关于七层负载均衡的入门介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
