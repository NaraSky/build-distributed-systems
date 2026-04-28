# 实现 Least-Connections Load Balancing

英文标题：Implement Least-Connections Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-1-least-connections>

课程：14. 负载均衡器
任务序号：11
短标题：Least-Connections
难度：intermediate
子主题：高级 Balancing Algorithms

## 中文导读

本题要求你完成 `实现 Least-Connections Load Balancing`。

重点关注：`least-connections`、`active connection tracking`、`load-based routing`、`atomic counters`、`variable request durations`。

建议先按提示逐步实现：Track active connections per backend: increment on 请求 start, decrement on 响应。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Least-connections load balancing routes each 请求 to the backend，包含the fewest active connections. This is superior to round-robin when 请求 durations vary significantly.

**Why least-connections?**
```
Round-robin problem:
  请求 1 → backend-1 (100ms duration)
  请求 2 → backend-2 (10ms duration)
  请求 3 → backend-3 (100ms duration)

  At t=50ms:
    backend-1: 1 active connection
    backend-2: 0 (completed)
    backend-3: 1 active connection

  请求 4 arrives → backend-1 (RR) → now has 2 active!
  Better: send to backend-2 (0 active)
```

**Connection tracking**:
```typescript
backendStates: Map<string, {
  activeConnections: number,
  totalRequests: number,
  lastUsed: timestamp
}>

function routeRequest(): string {
  // Find backend，包含minimum active connections
  let minBackend = null;
  let minConnections = Infinity;

 用于(const [backend, state] of backendStates) {
    if (state.activeConnections < minConnections) {
      minConnections = state.activeConnections;
      minBackend = backend;
    }
  }

  // Increment 计数器 atomically
  backendStates.get(minBackend).activeConnections++;
  return minBackend;
}

function requestComplete(backend: string) {
  backendStates.get(backend).activeConnections--;
}
```

**Example least-connections routing**:
```JSON
// Initial state: all backends have 0 connections
请求:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/data", "algorithm": "least-connections"}
响应: {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "active_connections": {"api-1": 1, "api-2": 0, "api-3": 0}}

// Second 请求 routes to api-2 (0 connections)
请求:  {"type": "http_request", "msg_id": 2, "method": "GET", "path": "/api/data", "algorithm": "least-connections"}
响应: {"type": "http_response", "in_reply_to": 2, "status": 200, "backend": "api-2", "active_connections": {"api-1": 1, "api-2": 1, "api-3": 0}}
```

## 涉及概念

- `least-connections`
- `active connection tracking`
- `load-based routing`
- `atomic counters`
- `variable request durations`

## 实现提示

- Track active connections per backend: increment on 请求 start, decrement on 响应
- Select backend，包含minimum active connections
- Use atomic counters用于thread-safe updates
- Better than round-robin when 请求 durations vary widely
- Example: long requests don't block other backends

## 测试用例

### 1. Route to backend，包含fewest connections

Should route to api-2 (2 connections, the minimum).

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":["api-1","api-2","api-3"],"algorithm":"least-connections"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/data","active_connections":{"api-1":5,"api-2":2,"api-3":8}}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Tie-breaking when connections equal

When all backends have equal connections, should use round-robin or consistent tie-breaking.

输入：

```json
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/data","active_connections":{"api-1":3,"api-2":3,"api-3":3}}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "backend": "api-1"}}
```

## 参考资料

- [Least-Connections Algorithm](https://www.nginx.com/blog/nginx-load-balancing-algorithms/)：NGINX documentation on load balancing algorithms

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
