# 添加 Health-Based Routing

英文标题：Add Health-Based Routing
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-12-5-health-routing>

课程：12. 代理
任务序号：5
短标题：Health Routing
难度：intermediate
子主题：Caching 代理

## 中文导读

本题要求你完成 `添加 Health-Based Routing`。

重点关注：`health checks`、`circuit breaker`、`failover`。

建议先按提示逐步实现：Periodically check backend health。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Add health-based routing，包含circuit breaker pattern:

1. Maintain list of backend servers
2. Periodically health-check each backend
3. Track consecutive failures per backend
4. Open circuit after N failures (stop sending traffic)
5. Periodically test，包含single 请求 (half-open)
6. Close circuit on success (resume normal traffic)

This improves reliability by routing away from failing backends.

## 概念说明

### Health Checks

Active health checks periodically probe backends，包含test requests. Passive checks observe real 请求 failures. Both inform routing decisions用于fast 故障 detection.

### Circuit Breaker

The circuit breaker prevents cascading failures. After enough failures, the circuit "opens"和requests fail immediately without trying the backend. After a 超时, one test 请求 checks recovery (half-open state).

## 涉及概念

- `health checks`
- `circuit breaker`
- `failover`

## 实现提示

- Periodically check backend health
- Track 故障 counts per backend
- Implement circuit breaker pattern

## 测试用例

### 1. Route to healthy

代理 has 3 backends: b1 (healthy), b2 (unhealthy, 5 failures), b3 (healthy). Health check marks b2 as down. Verify 代理 only routes requests to b1和b3, skipping unhealthy b2.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Open circuit on failures

Backend b1 initially healthy. Send requests that fail 5 times consecutively (threshold=3). After 3 failures, circuit should open用于b1. Verify 代理 stops sending traffic to b1 until circuit half-opens用于health check.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)：Martin Fowler on circuit breakers

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
