# 实现最少连接数负载均衡

英文标题：Implement Least-Connections Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-1-least-connections>

课程：14. 负载均衡器
任务序号：11
短标题：Least-Connections
难度：进阶
子主题：高级均衡算法

## 中文导读

本题要求你实现最少连接数（Least-Connections）负载均衡算法。轮询算法对每个请求一视同仁，但现实中请求的处理时间可能相差很大——有的几毫秒就完成了，有的要好几秒。最少连接数算法每次都把新请求分配给当前活跃连接最少的后端，从而自动适应这种差异，让负载真正均匀。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

最少连接数负载均衡将每个请求路由到活跃连接数最少的后端。当请求处理时间差异较大时，这种算法比轮询更优秀。

**为什么需要最少连接数**：
```
Round-robin problem:
  Request 1 → backend-1 (100ms duration)
  Request 2 → backend-2 (10ms duration)
  Request 3 → backend-3 (100ms duration)

  At t=50ms:
    backend-1: 1 active connection
    backend-2: 0 (completed)
    backend-3: 1 active connection

  Request 4 arrives → backend-1 (RR) → now has 2 active!
  Better: send to backend-2 (0 active)
```

上面的例子说明了轮询的问题：在 50 毫秒时，backend-2 已经空闲了，但轮询仍然把第 4 个请求分给了已经在忙的 backend-1。如果使用最少连接数算法，第 4 个请求会被分给空闲的 backend-2。

**连接跟踪**：
```typescript
backendStates: Map<string, {
  activeConnections: number,
  totalRequests: number,
  lastUsed: timestamp
}>

function routeRequest(): string {
  // Find backend with minimum active connections
  let minBackend = null;
  let minConnections = Infinity;

  for (const [backend, state] of backendStates) {
    if (state.activeConnections < minConnections) {
      minConnections = state.activeConnections;
      minBackend = backend;
    }
  }

  // Increment counter atomically
  backendStates.get(minBackend).activeConnections++;
  return minBackend;
}

function requestComplete(backend: string) {
  backendStates.get(backend).activeConnections--;
}
```

**最少连接数路由示例**：
```json
// Initial state: all backends have 0 connections
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/data", "algorithm": "least-connections"}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "active_connections": {"api-1": 1, "api-2": 0, "api-3": 0}}

// Second request routes to api-2 (0 connections)
Request:  {"type": "http_request", "msg_id": 2, "method": "GET", "path": "/api/data", "algorithm": "least-connections"}
Response: {"type": "http_response", "in_reply_to": 2, "status": 200, "backend": "api-2", "active_connections": {"api-1": 1, "api-2": 1, "api-3": 0}}
```

## 涉及概念

- `least-connections`
- `active connection tracking`
- `load-based routing`
- `atomic counters`
- `variable request durations`

## 实现提示

- 为每个后端跟踪活跃连接数：请求开始时计数加一，收到响应时计数减一
- 选择活跃连接数最少的后端
- 使用原子计数器保证线程安全
- 当请求处理时间差异较大时，效果优于轮询
- 比如：耗时较长的请求不会阻塞其他后端

## 测试用例

### 1. 将请求路由到连接数最少的后端

应将请求路由到 api-2（2 个连接，最少）。

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":["api-1","api-2","api-3"],"algorithm":"least-connections"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/data","active_connections":{"api-1":5,"api-2":2,"api-3":8}}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 连接数相同时的平局处理

当所有后端的连接数相同时，应使用轮询或其他一致的平局打破策略。

输入：

```json
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/data","active_connections":{"api-1":3,"api-2":3,"api-3":3}}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "backend": "api-1"}}
```

## 参考资料

- [Least-Connections Algorithm](https://www.nginx.com/blog/nginx-load-balancing-algorithms/)：关于各种负载均衡算法的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
