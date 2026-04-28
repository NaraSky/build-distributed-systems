# 实现 Power-of-Two-Choices Load Balancing

英文标题：Implement Power-of-Two-Choices Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-3-power-of-two-choices>

课程：14. 负载均衡器
任务序号：13
短标题：Power-of-Two-Choices
难度：advanced
子主题：高级 Balancing Algorithms

## 中文导读

本题要求你完成 `实现 Power-of-Two-Choices Load Balancing`。

重点关注：`power-of-two-choices`、`randomized load balancing`、`least-connections approximation`、`constant-time selection`、`scalability`。

建议先按提示逐步实现：Pick 2 random backends (with replacement)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Power-of-two-choices is a randomized load balancing algorithm that approximates least-connections，包含constant-time selection. Instead of checking all N backends, it randomly samples 2和picks the better one.

**The algorithm**:
```typescript
function selectBackend(backends: Backend[]): string {
  // Pick 2 random backends (with replacement)
  const backend1 = backends[randomInt(0, backends.length - 1)];
  const backend2 = backends[randomInt(0, backends.length - 1)];

  // Choose the one，包含fewer connections
  if (backend1.activeConnections <= backend2.activeConnections) {
    return backend1.name;
  } else {
    return backend2.name;
  }
}
```

**Why it works**:
- Checking 2 random backends gives you a lot of information
- Probability of picking the 2 worst backends is very low
- With 10 backends, checking 2 gives you the top 20% in expectation
- As N grows, the gap between checking 2和checking all shrinks

**Comparison**:
```
Algorithm           | Selection Time | Quality
--------------------|----------------|----------------
Round-robin         | O(1)          | Poor (no load awareness)
Least-connections   | O(N)          | Optimal
Power-of-two-choices| O(1)          | Near-optimal (~95% of optimal)

With 100 backends:
  Least-connections: 100 queries
  Power-of-two: 2 queries
  Speedup: 50x
  Quality loss: <5%
```

**Example power-of-two routing**:
```JSON
// Backends state:
{
  "backends": [
    {"name": "api-1", "connections": 10},
    {"name": "api-2", "connections": 5},
    {"name": "api-3", "connections": 8},
    {"name": "api-4", "connections": 12},
    {"name": "api-5", "connections": 3}
  ]
}

// 请求 1: randomly pick api-3 (8)和api-5 (3)
// Select api-5 (fewer connections)
请求:  {"type": "http_request", "msg_id": 1, "algorithm": "power-of-two-choices"}
响应: {"type": "http_response", "in_reply_to": 1, "backend": "api-5", "sampled": ["api-3", "api-5"], "selected": "api-5", "reason": "3 < 8 connections"}
```

## 涉及概念

- `power-of-two-choices`
- `randomized load balancing`
- `least-connections approximation`
- `constant-time selection`
- `scalability`

## 实现提示

- Pick 2 random backends (with replacement)
- Query their active connection counts
- Send 请求 to the backend，包含fewer connections
- Nearly as good as least-connections but O(1) instead of O(N)
- Prove this，包含a simulation or benchmark

## 测试用例

### 1. Power-of-two selects better of 2 random

Should sample 2 random backends和select the one，包含fewer connections. 响应 should include sampled backends.

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":[{"name":"api-1","connections":10},{"name":"api-2","connections":5},{"name":"api-3","connections":8}],"algorithm":"power-of-two-choices"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"algorithm":"power-of-two-choices"}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Comparison，包含least-connections

Power-of-two should achieve ~95% of least-connections quality (8.1 vs 7.67 average connections).

输入：

```json
{"src":"client","dest":"lb","body":{"type":"benchmark","msg_id":1,"algorithms":["least-connections","power-of-two-choices"],"backends":[{"name":"api-1","connections":10},{"name":"api-2","connections":5},{"name":"api-3","connections":8}],"requests":1000}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "benchmark_ok", "in_reply_to": 1, "results": {"least-connections": {"avg_connections": 7.67}, "power-of-two-choices": {"avg_connections": 8.1}}}}
```

## 参考资料

- [The Power of Two随机Choices](http://www.eecs.harvard.edu/~michaelm/postscripts/im2002b.pdf)：Original paper on the power-of-two-choices technique

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
