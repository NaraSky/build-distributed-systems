# 实现 Layer 7 HTTP 代理

英文标题：Implement Layer 7 HTTP Proxy
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-1-http-proxy>

课程：14. 负载均衡器
任务序号：6
短标题：HTTP 代理
难度：intermediate
子主题：Layer 7 Load Balancing

## 中文导读

本题要求你完成 `实现 Layer 7 HTTP 代理`。

重点关注：`layer 7 load balancing`、`HTTP proxy`、`request routing`、`header inspection`、`backend selection`。

建议先按提示逐步实现：Parse incoming HTTP requests to extract Host header和URL path。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Layer 7 load balancing operates at the HTTP application layer, inspecting headers和URL paths to make routing decisions. Unlike Layer 4 (TCP), L7 proxies understand HTTP semantics.

**HTTP 代理 architecture**:
```
客户端 → L7 代理 → Backend
  - Parse HTTP 请求
  - Inspect headers (Host, User-Agent, Cookies)
  - Inspect URL path (/api/users, /static/images)
  - Select backend based on rules
  - Forward 请求和return 响应
```

**请求 flow**:
```
1. 客户端 sends: GET /api/users HTTP/1.1
   Host: example.com

2. 代理 parses:
   - Method: GET
   - Path: /api/users
   - Host: example.com

3. 代理 routes to backend pool "api"

4. Backend responds: HTTP/1.1 200 OK
   {"users": [...]}

5. 代理 returns 响应 to 客户端
```

**Example 请求**:
```JSON
请求:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "headers": {"Host": "example.com", "User-Agent": "Mozilla"}}
响应: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"Content-Type": "application/JSON"}, "body": "{"users": [{"id": 1, "name": "Alice"}]}", "backend": "api-1"}
```

**Backend pool configuration**:
```JSON
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

- Parse incoming HTTP requests to extract Host header和URL path
- Maintain a backend pool，包含health status
- Select a backend based on routing rules
- Forward the 请求 to the backend和return the 响应
-处理connection pooling和keep-alive

## 测试用例

### 1. Route HTTP GET to correct backend

http_response should return status 200和indicate which backend handled the 请求 (e.g., api-1).

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","headers":{"Host":"example.com"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1"}}
```

### 2. Route based on URL path

Requests to /static/* should route to the static backend pool.

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/static/logo.png","headers":{"Host":"example.com"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "static-1"}}
```

## 参考资料

- [Layer 7 Load Balancing](https://www.nginx.com/resources/glossary/layer-7-load-balancing/)：Introduction to L7 load balancing，包含Nginx

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
