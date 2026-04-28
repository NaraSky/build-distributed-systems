# 实现熔断器

英文标题：Implement Circuit Breaking
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-4-circuit-breaking>

课程：14. 负载均衡器
任务序号：9
短标题：Circuit Breaking
难度：高级
子主题：七层负载均衡

## 中文导读

本题要求你实现熔断器（Circuit Breaker）模式。熔断器的工作原理就像家里的保险丝：当某个后端服务持续出错时，熔断器会"断开"，暂时停止向该服务发送请求，避免大量请求堆积在一个已经有问题的服务上，从而防止故障蔓延到整个系统。等待一段时间后，熔断器会试探性地放行一个请求，如果成功就恢复正常，否则继续保持断开状态。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

**熔断器的三种状态**：
- 关闭状态（CLOSED，正常）：请求正常转发到后端。在滑动窗口内跟踪失败次数。如果失败次数超过阈值，切换到打开状态。
- 打开状态（OPEN，熔断中）：所有请求立即快速失败，不再尝试访问后端。超时时间到达后，切换到半开状态。
- 半开状态（HALF_OPEN，试探中）：允许一个探测请求通过。如果成功，切换回关闭状态。如果失败，重新切换到打开状态。

**故障跟踪所需的字段**：
```typescript
state: "CLOSED" | "OPEN" | "HALF_OPEN";
failureCount: number;
lastFailureTime: number;
successCount: number;
// Configuration
failureThreshold: number = 5; // Open after 5 failures
timeout: number = 60000; // Try again after 60s
halfOpenMaxAttempts: number = 1; // One probe request
```

**熔断器指标示例**：
```json
"backend": "api-1",
"state": "OPEN",
"failure_count": 7,
"last_failure_time": 1680123456,
"opened_at": 1680123450,
"next_attempt_at": 1680123510
```

## 涉及概念

- `circuit breaker`
- `failure threshold`
- `half-open state`
- `automatic recovery`
- `cascade prevention`

## 实现提示

- 为每个后端跟踪失败次数：如果失败计数超过阈值（例如 5 次），打开熔断器
- 熔断器打开后：立即拒绝请求，不再尝试访问后端
- 超时时间到达后（例如 60 秒），进入半开状态：发送一个探测请求
- 如果探测成功，关闭熔断器；如果失败，重新打开熔断器
- 这种机制可以在后端过载时防止故障级联

## 测试用例

### 1. 达到失败阈值后熔断器打开

连续 5 次失败后，熔断器应打开，直接返回 503 而不尝试访问后端。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","simulate_failures":5}}
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/users"}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 500, "backend": "api-1"}}
```

### 2. 探测成功后熔断器关闭

在半开状态下探测成功后，熔断器应切换回关闭状态。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","circuit_state":"HALF_OPEN","probe_result":"success"}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "circuit_state": "CLOSED"}}
```

## 参考资料

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)：关于熔断器模式的经典讲解

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
