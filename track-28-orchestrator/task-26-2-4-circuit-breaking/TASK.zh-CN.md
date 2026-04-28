# 实现 Circuit Breaking in 服务 Mesh

英文标题：Implement Circuit Breaking in Service Mesh
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-4-circuit-breaking>

课程：28. 编排器：容器调度与服务网格
任务序号：9
短标题：Circuit Breaking
难度：advanced
子主题：服务 Mesh

## 中文导读

本题要求你完成 `实现 Circuit Breaking in 服务 Mesh`。

重点关注：`circuit breaker`、`fail fast`、`half-open state`、`cascading failures`、`service resilience`。

建议先按提示逐步实现：Three states: closed (calls pass through), open (fail immediately), half-open (test one call)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a downstream service is failing, continuing to call it wastes resources和slows down your service. A circuit breaker detects this和**fails fast**: instead of waiting用于a 超时, it immediately returns an error和periodically tests whether the service has recovered.

The circuit breaker has three states:

```
CLOSED  --(故障 threshold exceeded)--> OPEN
OPEN    --(after 超时)--> HALF-OPEN
HALF-OPEN --(success)--> CLOSED
HALF-OPEN --(故障)--> OPEN
```

Implement a 节点 that enforces this state machine per service:

```JSON
// Enough failures -> breaker opens
{ "type": "call", "msg_id": 1,
  "force_failures": 5 }
-> { "type": "circuit_breaker_open", "in_reply_to": 1,
    "service": "service-b", "failures": 5 }

// Fail fast while circuit is open
{ "type": "call", "msg_id": 2, "state": "open" }
-> { "type": "error", "in_reply_to": 2,
    "error": "Circuit breaker OPEN", "service": "service-b" }

// Half-open probe succeeds -> close the breaker
{ "type": "call", "msg_id": 3,
  "state": "half_open", "force_success": true }
-> { "type": "circuit_breaker_closed", "in_reply_to": 3,
    "service": "service-b", "state": "closed" }
```

## 涉及概念

- `circuit breaker`
- `fail fast`
- `half-open state`
- `cascading failures`
- `service resilience`

## 实现提示

- Three states: closed (calls pass through), open (fail immediately), half-open (test one call)
- Transition to open when consecutive failures >= threshold
- In half-open, allow one call through; close on success, re-open on 故障
- Fail fast: when open, return error immediately without calling the downstream service
- Track failures per service so each service has its own independent circuit breaker

## 测试用例

### 1. Circuit breaker opens after failures

Circuit breaker should open after 5 consecutive failures.

输入：

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"force_failures":5}}
```

期望输出：

```text
{"type": "circuit_breaker_open", "in_reply_to": 1, "service": "service-b", "failures": 5}
```

### 2. Circuit breaker recovers on success

Successful probe in half-open state should close the breaker.

输入：

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"state":"half_open","force_success":true}}
```

期望输出：

```text
{"type": "circuit_breaker_closed", "in_reply_to": 1, "service": "service-b", "state": "closed"}
```

## 参考资料

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)：Martin Fowler's explanation of the circuit breaker pattern

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
