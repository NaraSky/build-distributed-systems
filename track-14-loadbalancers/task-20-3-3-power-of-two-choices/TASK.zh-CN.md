# 实现二选一负载均衡

英文标题：Implement Power-of-Two-Choices Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-3-power-of-two-choices>

课程：14. 负载均衡器
任务序号：13
短标题：Power-of-Two-Choices
难度：高级
子主题：高级均衡算法

## 中文导读

本题要求你实现"二选一"（Power-of-Two-Choices）负载均衡算法。这是一个非常巧妙的随机化算法：每次收到请求时，随机挑选两个后端，然后把请求发给连接数较少的那个。听起来很简单，但数学上已经证明，仅仅"随机选两个、挑好的那个"就能达到接近最优的效果（约 95%），而时间复杂度只有常数级别。当后端数量很多时，这种方法比遍历所有后端找最少连接的做法快得多。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

"二选一"是一种随机化负载均衡算法，能以常数时间复杂度近似实现最少连接数的效果。它不需要检查所有 N 个后端，而是随机抽样 2 个，选择其中较优的那个。

**算法实现**：
```typescript
function selectBackend(backends: Backend[]): string {
  // Pick 2 random backends (with replacement)
  const backend1 = backends[randomInt(0, backends.length - 1)];
  const backend2 = backends[randomInt(0, backends.length - 1)];

  // Choose the one with fewer connections
  if (backend1.activeConnections <= backend2.activeConnections) {
    return backend1.name;
  } else {
    return backend2.name;
  }
}
```

**为什么有效**：
- 随机检查 2 个后端就能获取大量信息
- 同时选中两个最差后端的概率非常低
- 对于 10 个后端，检查 2 个就能在期望上选到前 20% 的后端
- 随着后端数量增加，"检查 2 个"与"检查全部"的效果差距越来越小

**各算法对比**：
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

**二选一路由示例**：
```json
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

// Request 1: randomly pick api-3 (8) and api-5 (3)
// Select api-5 (fewer connections)
Request:  {"type": "http_request", "msg_id": 1, "algorithm": "power-of-two-choices"}
Response: {"type": "http_response", "in_reply_to": 1, "backend": "api-5", "sampled": ["api-3", "api-5"], "selected": "api-5", "reason": "3 < 8 connections"}
```

## 涉及概念

- `power-of-two-choices`
- `randomized load balancing`
- `least-connections approximation`
- `constant-time selection`
- `scalability`

## 实现提示

- 随机选取 2 个后端（允许重复选取同一个）
- 查询它们的活跃连接数
- 将请求发送到连接数较少的那个后端
- 效果接近最少连接数算法，但时间复杂度从 O(N) 降到了 O(1)
- 可以通过模拟或基准测试来验证效果

## 测试用例

### 1. 从两个随机后端中选择较优的

应随机抽取 2 个后端，选择连接数较少的那个。响应中应包含被抽样的后端信息。

输入：

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":[{"name":"api-1","connections":10},{"name":"api-2","connections":5},{"name":"api-3","connections":8}],"algorithm":"power-of-two-choices"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"algorithm":"power-of-two-choices"}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 与最少连接数算法的效果对比

"二选一"应达到最少连接数约 95% 的效果（平均连接数 8.1 对比 7.67）。

输入：

```json
{"src":"client","dest":"lb","body":{"type":"benchmark","msg_id":1,"algorithms":["least-connections","power-of-two-choices"],"backends":[{"name":"api-1","connections":10},{"name":"api-2","connections":5},{"name":"api-3","connections":8}],"requests":1000}}
```

期望输出：

```text
{"src": "lb", "dest": "client", "body": {"type": "benchmark_ok", "in_reply_to": 1, "results": {"least-connections": {"avg_connections": 7.67}, "power-of-two-choices": {"avg_connections": 8.1}}}}
```

## 参考资料

- [The Power of Two Random Choices](http://www.eecs.harvard.edu/~michaelm/postscripts/im2002b.pdf)：关于"二选一"技术的原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
