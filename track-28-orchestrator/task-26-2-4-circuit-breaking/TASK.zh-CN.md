# 实现服务网格中的熔断器

英文标题：Implement Circuit Breaking in Service Mesh
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-4-circuit-breaking>

课程：28. 编排器：容器调度与服务网格
任务序号：9
短标题：Circuit Breaking
难度：高级
子主题：Service Mesh

## 中文导读

这道题要求你实现一个按服务维护状态机的熔断器节点。当下游服务出了问题，如果你还一直调用它，只会白白浪费资源并拖慢自己的响应速度。熔断器能自动检测到这种情况，立刻停止调用故障服务，并定期探测它是否恢复。这就像家里的保险丝，在电路异常时自动断开以保护整个电路。

## 题目说明

当下游服务出现故障时，继续调用它只会浪费资源并拖慢你的服务。熔断器（Circuit Breaker）检测到故障后会**快速失败**：不再等待超时，而是立即返回错误，并周期性地探测下游服务是否已恢复。

熔断器有三个状态：

```
关闭（CLOSED）  --（失败次数超过阈值）--> 打开（OPEN）
打开（OPEN）    --（等待超时后）--> 半开（HALF-OPEN）
半开（HALF-OPEN） --（探测成功）--> 关闭（CLOSED）
半开（HALF-OPEN） --（探测失败）--> 打开（OPEN）
```

请实现一个按服务维护熔断器状态机的节点：

```json
// 失败次数足够多 -> 熔断器打开
{ "type": "call", "msg_id": 1,
  "force_failures": 5 }
-> { "type": "circuit_breaker_open", "in_reply_to": 1,
    "service": "service-b", "failures": 5 }

// 熔断器打开时快速失败
{ "type": "call", "msg_id": 2, "state": "open" }
-> { "type": "error", "in_reply_to": 2,
    "error": "Circuit breaker OPEN", "service": "service-b" }

// 半开状态下探测成功 -> 关闭熔断器
{ "type": "call", "msg_id": 3,
  "state": "half_open", "force_success": true }
-> { "type": "circuit_breaker_closed", "in_reply_to": 3,
    "service": "service-b", "state": "closed" }
```

## 概念说明

熔断器的工作方式和家用保险丝很像。正常情况下保险丝是闭合的，电流正常通过（关闭状态）。一旦电流过大，保险丝就会熔断，切断电路以保护电器（打开状态）。过一段时间后，你会试着把保险丝合上，看看问题是否解决了（半开状态）。如果一切正常就恢复使用，如果还是有问题就再次断开。在分布式系统中，"电流过大"就对应着"下游服务连续失败"。

## 涉及概念

- `circuit breaker`
- `fail fast`
- `half-open state`
- `cascading failures`
- `service resilience`

## 实现提示

- 三个状态：关闭（请求正常通过）、打开（立即返回失败）、半开（放行一个请求进行探测）
- 当连续失败次数达到或超过阈值时，转换到打开状态
- 在半开状态下，只放行一个请求：成功则关闭熔断器，失败则重新打开
- 快速失败：打开状态下立即返回错误，不再调用下游服务
- 按服务独立追踪失败次数，每个服务维护自己独立的熔断器

## 测试用例

### 1. 熔断器在多次失败后打开

连续 5 次失败后熔断器应打开。

输入：

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"force_failures":5}}
```

期望输出：

```text
{"type": "circuit_breaker_open", "in_reply_to": 1, "service": "service-b", "failures": 5}
```

### 2. 熔断器在探测成功后恢复

半开状态下的探测成功应关闭熔断器。

输入：

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"state":"half_open","force_success":true}}
```

期望输出：

```text
{"type": "circuit_breaker_closed", "in_reply_to": 1, "service": "service-b", "state": "closed"}
```

## 参考资料

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)：Martin Fowler 对熔断器模式的详细解释

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
