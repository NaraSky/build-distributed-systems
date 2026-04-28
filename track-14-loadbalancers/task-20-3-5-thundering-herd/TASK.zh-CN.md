# Simulate Thundering Herd，包含Circuit Breaking

英文标题：Simulate Thundering Herd，包含Circuit Breaking
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-5-thundering-herd>

课程：14. 负载均衡器
任务序号：15
短标题：Thundering Herd
难度：advanced
子主题：高级 Balancing Algorithms

## 中文导读

本题要求你完成 `Simulate Thundering Herd，包含Circuit Breaking`。

重点关注：`thundering herd`、`cascading failures`、`exponential backoff`、`graceful degradation`、`circuit breaking`。

建议先按提示逐步实现：Simulate: backend-4 fails, 10,000 connections suddenly redistribute to remaining backends。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The thundering herd problem occurs when a large number of clients simultaneously 重试 after a backend 故障, overwhelming the remaining backends和causing cascading failures.

**The problem**:
```
Normal state:
  backend-1: 1000 req/s
  backend-2: 1000 req/s
  backend-3: 1000 req/s
  backend-4: 1000 req/s

backend-4 fails:
  All 4000 req/s from backend-4 重试 immediately
  backend-1, 2, 3 now receive 2333 req/s each (overload!)
  They fail under load
  All backends down = outage
```

**Circuit breaking + exponential backoff**:
```
Circuit breaker:
  - Detect backend-4 故障 rate > 50%
  - Open circuit: stop sending requests to backend-4
  - Traffic redistributes gradually (not all at once)

Exponential backoff (客户端-side):
  - 重试 1: 100ms delay
  - 重试 2: 200ms delay
  - 重试 3: 400ms delay
  - 重试 4: 800ms delay
  - Spreads out 重试 load over time

Result:
  - backend-1, 2, 3 handle 1333 req/s each (manageable)
  - No cascading 故障
```

**Example thundering herd simulation**:
```JSON
请求:  {"type": "simulate_thundering_herd", "msg_id": 1, "backends": ["b1", "b2", "b3", "b4"], "requests_per_second": 4000, "fail_backend": "b4", "duration_ms": 10000, "with_circuit_breaker": false}
响应: {"type": "simulation_complete", "in_reply_to": 1, "results": {"without_circuit_breaker": {"cascading_failures": true, "backends_down": ["b1", "b2", "b3"], "p99_latency_ms": 5000, "error_rate": 1.0}}}

请求:  {"type": "simulate_thundering_herd", "msg_id": 2, "backends": ["b1", "b2", "b3", "b4"], "requests_per_second": 4000, "fail_backend": "b4", "duration_ms": 10000, "with_circuit_breaker": true, "with_exponential_backoff": true}
响应: {"type": "simulation_complete", "in_reply_to": 2, "results": {"with_protections": {"cascading_failures": false, "backends_down": ["b4"], "p99_latency_ms": 150, "error_rate": 0.25}}}
```

**Metrics to track**:
- Requests per second (per backend)
- Error rate (5xx responses)
- Latency percentiles (p50, p99, p99.9)
- Circuit breaker state transitions
- 重试 attempt distribution

## 涉及概念

- `thundering herd`
- `cascading failures`
- `exponential backoff`
- `graceful degradation`
- `circuit breaking`

## 实现提示

- Simulate: backend-4 fails, 10,000 connections suddenly redistribute to remaining backends
- Without circuit breaking: remaining backends overload和fail
- With circuit breaking: failed backend is removed from pool immediately
- With exponential backoff: clients 重试，包含increasing delays
- Measure: requests/sec, error rate, latency p99 before和after 故障

## 测试用例

### 1. Thundering herd without protections

Without circuit breaking, thundering herd should cause all backends to fail (cascading 故障).

输入：

```json
{"src":"client","dest":"simulator","body":{"type":"simulate_thundering_herd","msg_id":1,"backends":["b1","b2","b3","b4"],"requests_per_second":4000,"fail_backend":"b4","with_circuit_breaker":false}}
```

期望输出：

```text
{"src": "simulator", "dest": "client", "body": {"type": "simulation_complete", "in_reply_to": 1, "results": {"cascading_failures": true, "all_backends_failed": true, "error_rate": 1.0}}}
```

### 2. Circuit breaking prevents cascade

With circuit breaking, only b4 should fail. b1, b2, b3 should stay healthy.

输入：

```json
{"src":"client","dest":"simulator","body":{"type":"simulate_thundering_herd","msg_id":1,"backends":["b1","b2","b3","b4"],"requests_per_second":4000,"fail_backend":"b4","with_circuit_breaker":true}}
```

期望输出：

```text
{"src": "simulator", "dest": "client", "body": {"type": "simulation_complete", "in_reply_to": 1, "results": {"cascading_failures": false, "failed_backends": ["b4"], "error_rate": 0.25}}}
```

## 参考资料

- [Thundering Herd Problem](https://www.awsarchitectureblog.com/2015/03/05/thundering-herds.html)：AWS blog on thundering herd和mitigation strategies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
