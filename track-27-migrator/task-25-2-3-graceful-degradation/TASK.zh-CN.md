# 实现 Graceful API Degradation

英文标题：Implement Graceful API Degradation
网页：<https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-3-graceful-degradation>

课程：27. 迁移器：数据与协议演进
任务序号：8
短标题：Graceful Degradation
难度：advanced
子主题：Protocol和API Evolution

## 中文导读

本题要求你完成 `实现 Graceful API Degradation`。

重点关注：`graceful degradation`、`circuit breaker`、`fallback cache`、`feature flags`、`request queuing`。

建议先按提示逐步实现：Circuit breaker: after threshold failures, return cached data instead of calling the failing service。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Graceful degradation keeps your API functional even when downstream services are failing. Instead of returning errors, you serve cached data, disable non-critical features, or 队列 requests用于later processing. The user gets a slightly degraded experience instead of a complete outage.

Implement a 节点 that degrades gracefully under 故障 conditions:

```JSON
// Service failing -> open circuit breaker, return cached data
{ "type": "get_user", "msg_id": 1,
  "user_id": 123, "force_failures": 6 }
-> { "type": "user_response", "in_reply_to": 1,
    "user": {"id": 123, "name": "John Doe"},
    "circuit_state": "open", "from_cache": true }

// Dependency down -> return stale cached product
{ "type": "get_product", "msg_id": 2,
  "product_id": 123, "service_unavailable": true }
-> { "type": "product_response", "in_reply_to": 2,
    "product": {"id": 123, "name": "Product"},
    "_cached": true }

// High load -> disable expensive features
{ "type": "set_mode", "msg_id": 3,
  "mode": "degraded", "cpu_usage": 85 }
-> { "type": "mode_changed", "in_reply_to": 3,
    "mode": "degraded",
    "disabled_features": ["recommendations", "search"] }
```

## 涉及概念

- `graceful degradation`
- `circuit breaker`
- `fallback cache`
- `feature flags`
- `request queuing`

## 实现提示

- Circuit breaker: after threshold failures, return cached data instead of calling the failing service
- Cached fallback: return stale data，包含_cached: true when a dependency is down
- Feature flags: disable expensive non-critical features (recommendations, search) under high load
- 请求 queuing: accept the 请求和队列 it用于later processing when the service is down
- circuit_state: "open" means the circuit breaker is tripped和using the fallback

## 测试用例

### 1. Circuit breaker opens after failures

After 6 failures the circuit opens和serves cached data.

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_user","msg_id":1,"user_id":123,"force_failures":6}}
```

期望输出：

```text
{"type": "user_response", "in_reply_to": 1, "user": {"id": 123, "name": "John Doe"}, "circuit_state": "open", "from_cache": true}
```

### 2. Fallback to cached data

Service unavailable should return stale cached data.

输入：

```json
{"src":"client","dest":"api","body":{"type":"get_product","msg_id":1,"product_id":123,"service_unavailable":true}}
```

期望输出：

```text
{"type": "product_response", "in_reply_to": 1, "product": {"id": 123, "name": "Product"}, "_cached": true}
```

## 参考资料

- [Graceful Degradation](https://docs.microsoft.com/en-us/azure/architecture/patterns/bulkhead)：Bulkhead和circuit breaker patterns用于graceful degradation
- [Graceful Degradation](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)：AWS builders library on graceful degradation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
