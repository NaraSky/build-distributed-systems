# 模拟惊群效应与熔断保护

英文标题：Simulate Thundering Herd with Circuit Breaking
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-5-thundering-herd>

课程：14. 负载均衡器
任务序号：15
短标题：Thundering Herd
难度：高级
子主题：高级均衡算法

## 中文导读

本题要求你模拟并解决"惊群效应"（Thundering Herd）问题。想象一头牛倒下了，整个牛群受惊四散奔逃，踩踏了更多的牛——这就是惊群效应的形象比喻。在分布式系统中，当一台后端宕机时，原本发往它的大量请求会瞬间涌向其他后端，如果处理不当，这些后端也会被压垮，引发连锁故障，最终导致全部后端崩溃。你需要用熔断器和指数退避来防止这种灾难。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

惊群效应发生在大量客户端在后端故障后同时重试的场景下，突发的重试请求会压垮剩余的后端，导致级联故障。

**问题描述**：
```
Normal state:
  backend-1: 1000 req/s
  backend-2: 1000 req/s
  backend-3: 1000 req/s
  backend-4: 1000 req/s

backend-4 fails:
  All 4000 req/s from backend-4 retry immediately
  backend-1, 2, 3 now receive 2333 req/s each (overload!)
  They fail under load
  All backends down = outage
```

正常情况下每台后端处理 1000 请求/秒。当 backend-4 故障时，它的 4000 请求/秒立刻重试并涌向其余 3 台后端，每台变成 2333 请求/秒，超出处理能力，最终全部崩溃。

**熔断器 + 指数退避的解决方案**：
```
Circuit breaker:
  - Detect backend-4 failure rate > 50%
  - Open circuit: stop sending requests to backend-4
  - Traffic redistributes gradually (not all at once)

Exponential backoff (client-side):
  - Retry 1: 100ms delay
  - Retry 2: 200ms delay
  - Retry 3: 400ms delay
  - Retry 4: 800ms delay
  - Spreads out retry load over time

Result:
  - backend-1, 2, 3 handle 1333 req/s each (manageable)
  - No cascading failure
```

熔断器快速检测到 backend-4 的故障并切断对它的请求，流量逐步（而非瞬间）重新分配。指数退避让客户端的重试间隔逐渐加大，将重试负载分散到更长的时间段内。最终每台健康后端只需处理 1333 请求/秒，在可承受范围内，避免了级联故障。

**惊群模拟示例**：
```json
Request:  {"type": "simulate_thundering_herd", "msg_id": 1, "backends": ["b1", "b2", "b3", "b4"], "requests_per_second": 4000, "fail_backend": "b4", "duration_ms": 10000, "with_circuit_breaker": false}
Response: {"type": "simulation_complete", "in_reply_to": 1, "results": {"without_circuit_breaker": {"cascading_failures": true, "backends_down": ["b1", "b2", "b3"], "p99_latency_ms": 5000, "error_rate": 1.0}}}

Request:  {"type": "simulate_thundering_herd", "msg_id": 2, "backends": ["b1", "b2", "b3", "b4"], "requests_per_second": 4000, "fail_backend": "b4", "duration_ms": 10000, "with_circuit_breaker": true, "with_exponential_backoff": true}
Response: {"type": "simulation_complete", "in_reply_to": 2, "results": {"with_protections": {"cascading_failures": false, "backends_down": ["b4"], "p99_latency_ms": 150, "error_rate": 0.25}}}
```

**需要跟踪的指标**：
- 每秒请求数（按后端统计）
- 错误率（5xx 响应的比例）
- 延迟分位数（p50、p99、p99.9）
- 熔断器状态变迁
- 重试次数分布

## 涉及概念

- `thundering herd`
- `cascading failures`
- `exponential backoff`
- `graceful degradation`
- `circuit breaking`

## 实现提示

- 模拟场景：backend-4 故障，10000 个连接突然重新分配到剩余后端
- 无熔断保护：剩余后端过载并相继故障
- 有熔断保护：故障后端被立即移出后端池
- 有指数退避：客户端以递增的延迟间隔进行重试
- 衡量指标：故障前后的每秒请求数、错误率和 p99 延迟

## 测试用例

### 1. 无保护措施下的惊群效应

没有熔断器时，惊群效应应导致所有后端崩溃（级联故障）。

输入：

```json
{"src":"client","dest":"simulator","body":{"type":"simulate_thundering_herd","msg_id":1,"backends":["b1","b2","b3","b4"],"requests_per_second":4000,"fail_backend":"b4","with_circuit_breaker":false}}
```

期望输出：

```text
{"src": "simulator", "dest": "client", "body": {"type": "simulation_complete", "in_reply_to": 1, "results": {"cascading_failures": true, "all_backends_failed": true, "error_rate": 1.0}}}
```

### 2. 熔断器防止级联故障

启用熔断器后，只有 b4 应故障，b1、b2、b3 应保持健康。

输入：

```json
{"src":"client","dest":"simulator","body":{"type":"simulate_thundering_herd","msg_id":1,"backends":["b1","b2","b3","b4"],"requests_per_second":4000,"fail_backend":"b4","with_circuit_breaker":true}}
```

期望输出：

```text
{"src": "simulator", "dest": "client", "body": {"type": "simulation_complete", "in_reply_to": 1, "results": {"cascading_failures": false, "failed_backends": ["b4"], "error_rate": 0.25}}}
```

## 参考资料

- [Thundering Herd Problem](https://www.awsarchitectureblog.com/2015/03/05/thundering-herds.html)：关于惊群效应及其缓解策略的详细介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
