# 实现 Consistent Hashing用于Load Balancing

英文标题：Implement Consistent Hashing用于Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-4-consistent-hashing-lb>

课程：14. 负载均衡器
任务序号：14
短标题：Consistent Hashing LB
难度：advanced
子主题：高级 Balancing Algorithms

## 中文导读

本题要求你完成 `实现 Consistent Hashing用于Load Balancing`。

重点关注：`consistent hashing`、`session affinity`、`cache coherency`、`minimal disruption`、`backend additions/removals`。

建议先按提示逐步实现：Hash client_id or session_id to a point on the hash ring。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Consistent hashing用于load balancing ensures that the same 客户端 always routes to the same backend. This is useful用于caching layers where session state or 缓存 locality matters.

**Why consistent hashing用于LB?**
```
Problem: modulo hashing routes change when backends change
  client_1 → hash("client_1") % 3 = backend-1
  client_2 → hash("client_2") % 3 = backend-2

  Add backend-4:
  client_1 → hash("client_1") % 4 = backend-3 ❌ Different!
  All clients remap = 缓存 cold miss

Solution: consistent hashing
  client_1 → hash ring → backend-1
  client_2 → hash ring → backend-2

  Add backend-4:
  client_1 → hash ring → backend-1 ✓ Same!
  Only 25% of clients remap
```

**Algorithm**:
```typescript
function routeClient(clientId: string, backends: Backend[]): string {
  // Hash 客户端 ID to point on ring
  const clientPoint = hash(clientId) % 2^32;

  // Place backends on ring
  const backendPoints = backends.map(b => ({
    backend: b.name,
    point: hash(b.name) % 2^32
  }));

  // Sort by point
  backendPoints.sort((a, b) => a.point - b.point);

  // Find first backend clockwise from 客户端 point
 用于(const bp of backendPoints) {
    if (bp.point >= clientPoint) {
      return bp.backend;
    }
  }

  // Wrap around to first backend
  return backendPoints[0].backend;
}
```

**Example consistent hashing**:
```JSON
// Hash ring (simplified):
// 0°    : backend-1
// 120°  : backend-2
// 240°  : backend-3

// 客户端 requests:
请求:  {"type": "http_request", "msg_id": 1, "client_id": "alice", "path": "/api/data", "algorithm": "consistent-hash"}
响应: {"type": "http_response", "in_reply_to": 1, "backend": "backend-2", "hash_ring_position": 45}

// Same 客户端 always routes to same backend:
请求:  {"type": "http_request", "msg_id": 2, "client_id": "alice", "path": "/api/data", "algorithm": "consistent-hash"}
响应: {"type": "http_response", "in_reply_to": 2, "backend": "backend-2", "hash_ring_position": 45}

// Different 客户端 routes to potentially different backend:
请求:  {"type": "http_request", "msg_id": 3, "client_id": "bob", "path": "/api/data", "algorithm": "consistent-hash"}
响应: {"type": "http_response", "in_reply_to": 3, "backend": "backend-1", "hash_ring_position": 300}
```

## 涉及概念

- `consistent hashing`
- `session affinity`
- `cache coherency`
- `minimal disruption`
- `backend additions/removals`

## 实现提示

- Hash client_id or session_id to a point on the hash ring
- Route to the first backend clockwise from that point
- Same 客户端 always routes to same backend (sticky routing)
- When backend added, only 1/N of clients remap
- Use virtual 节点用于better distribution

## 测试用例

### 1. Same client always routes to same backend

All 3 requests from alice should route to the same backend.

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

### 2. Backend addition causes minimal remapping

Adding b4 should only remap ~25% of clients (1-3 clients), not all 10.

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

- [Consistent Hashing用于Load Balancing](https://www.nginx.com/blog/nginx-load-balancing-algorithms/)：NGINX documentation on consistent hashing load balancing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
