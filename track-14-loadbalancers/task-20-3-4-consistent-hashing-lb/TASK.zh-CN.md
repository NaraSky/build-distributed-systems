# 实现一致性哈希负载均衡

英文标题：Implement Consistent Hashing for Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-4-consistent-hashing-lb>

课程：14. 负载均衡器
任务序号：14
短标题：Consistent Hashing LB
难度：高级
子主题：高级均衡算法

## 中文导读

本题要求你实现基于一致性哈希（Consistent Hashing）的负载均衡。核心目标是让同一个客户端的请求始终路由到同一个后端，这在缓存和会话场景下非常重要。普通的取模哈希在后端数量变化时会导致几乎所有映射失效，而一致性哈希通过"哈希环"的设计，在后端增减时只影响少量客户端的路由，大大减少了缓存失效和会话丢失的问题。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

一致性哈希负载均衡确保同一客户端始终路由到同一后端。这在缓存层中非常有用，因为会话状态或缓存的局部性很重要。

**为什么负载均衡需要一致性哈希**：
```
Problem: modulo hashing routes change when backends change
  client_1 → hash("client_1") % 3 = backend-1
  client_2 → hash("client_2") % 3 = backend-2

  Add backend-4:
  client_1 → hash("client_1") % 4 = backend-3 ❌ Different!
  All clients remap = cache cold miss

Solution: consistent hashing
  client_1 → hash ring → backend-1
  client_2 → hash ring → backend-2

  Add backend-4:
  client_1 → hash ring → backend-1 ✓ Same!
  Only 25% of clients remap
```

上面的例子说明了问题：使用取模哈希时，新增一台后端就会导致所有客户端的映射关系改变，缓存全部失效。而一致性哈希只会影响约 25% 的客户端。

**算法实现**：
```typescript
function routeClient(clientId: string, backends: Backend[]): string {
  // Hash client ID to point on ring
  const clientPoint = hash(clientId) % 2^32;

  // Place backends on ring
  const backendPoints = backends.map(b => ({
    backend: b.name,
    point: hash(b.name) % 2^32
  }));

  // Sort by point
  backendPoints.sort((a, b) => a.point - b.point);

  // Find first backend clockwise from client point
  for (const bp of backendPoints) {
    if (bp.point >= clientPoint) {
      return bp.backend;
    }
  }

  // Wrap around to first backend
  return backendPoints[0].backend;
}
```

**一致性哈希示例**：
```json
// Hash ring (simplified):
// 0°    : backend-1
// 120°  : backend-2
// 240°  : backend-3

// Client requests:
Request:  {"type": "http_request", "msg_id": 1, "client_id": "alice", "path": "/api/data", "algorithm": "consistent-hash"}
Response: {"type": "http_response", "in_reply_to": 1, "backend": "backend-2", "hash_ring_position": 45}

// Same client always routes to same backend:
Request:  {"type": "http_request", "msg_id": 2, "client_id": "alice", "path": "/api/data", "algorithm": "consistent-hash"}
Response: {"type": "http_response", "in_reply_to": 2, "backend": "backend-2", "hash_ring_position": 45}

// Different client routes to potentially different backend:
Request:  {"type": "http_request", "msg_id": 3, "client_id": "bob", "path": "/api/data", "algorithm": "consistent-hash"}
Response: {"type": "http_response", "in_reply_to": 3, "backend": "backend-1", "hash_ring_position": 300}
```

## 涉及概念

- `consistent hashing`
- `session affinity`
- `cache coherency`
- `minimal disruption`
- `backend additions/removals`

## 实现提示

- 将客户端标识或会话标识哈希到哈希环上的一个点
- 沿顺时针方向找到第一个后端，将请求路由到它
- 同一客户端始终路由到同一后端（粘性路由）
- 新增后端时，只有约 1/N 的客户端需要重新映射
- 使用虚拟节点以获得更均匀的分布

## 测试用例

### 1. 同一客户端始终路由到同一后端

来自 alice 的所有 3 个请求都应路由到同一个后端。

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":["backend-1","backend-2","backend-3"],"algorithm":"consistent-hash"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"client_id":"alice"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":3,"client_id":"alice"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":4,"client_id":"alice"}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 新增后端时最小化重新映射

新增 b4 后，只应有约 25% 的客户端（10 个中的 1-3 个）被重新映射，而不是全部 10 个。

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":["b1","b2","b3"],"algorithm":"consistent-hash"}}
{"src":"client","dest":"lb","body":{"type":"test_remap","msg_id":2,"new_backend":"b4","clients":["c1","c2","c3","c4","c5","c6","c7","c8","c9","c10"]}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

## 参考资料

- [Consistent Hashing for Load Balancing](https://www.nginx.com/blog/nginx-load-balancing-algorithms/)：关于一致性哈希负载均衡的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
