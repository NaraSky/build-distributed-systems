# 实现 Circuit Breaking

英文标题：Implement Circuit Breaking
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-4-circuit-breaking>

课程：14. 负载均衡器
任务序号：9
短标题：Circuit Breaking
难度：advanced
子主题：Layer 7 Load Balancing

## 中文导读

本题要求你完成 `实现 Circuit Breaking`。

重点关注：`circuit breaker`、`failure threshold`、`half-open state`、`automatic recovery`、`cascade prevention`。

建议先按提示逐步实现：Track failures per backend: if failure_count > threshold (e.g., 5), open circuit。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

**Circuit states**:. ```. CLOSED (normal). - Requests pass through to backend. - Track failures in a sliding window. - If failures > threshold → OPEN. OPEN (failing). - All requests fail fast (no backend attempts). - After 超时 → HALF_OPEN. HALF_OPEN (testing). - Allow one probe 请求 through. - If success → CLOSED. - If 故障 → OPEN. ```. **故障 tracking**:. ```typescript. state: "CLOSED" | "OPEN" | "HALF_OPEN";. failureCount: number;. lastFailureTime: number;. successCount: number;. // Configuration. failureThreshold: number = 5; // Open after 5 failures. 超时: number = 60000; // Try again after 60s. halfOpenMaxAttempts: number = 1; // One probe 请求. ```. **Example circuit breaking**:. ```JSON. // Backend is healthy (circuit closed):. // Backend starts failing (5 failures in 30s):. // After 60s 超时 (half-open):. ```. **Circuit breaker metrics**:. ```JSON. "backend": "api-1",. "state": "OPEN",. "failure_count": 7,. "last_failure_time": 1680123456,. "opened_at": 1680123450,. "next_attempt_at": 1680123510. ```

## 涉及概念

- `circuit breaker`
- `failure threshold`
- `half-open state`
- `automatic recovery`
- `cascade prevention`

## 实现提示

- Track failures per backend: if failure_count > threshold (e.g., 5), open circuit
- Open circuit: reject requests immediately without trying backend
- After 超时 (e.g., 60s), enter half-open state: send one probe 请求
- If probe succeeds, close circuit; if fails, reopen circuit
- This prevents cascading failures when a backend is overwhelmed

## 测试用例

### 1. Circuit opens after threshold failures

After 5 failures, circuit should open和return 503 without attempting backend.

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","simulate_failures":5}}
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/users"}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 500, "backend": "api-1"}}
```

### 2. Circuit closes after successful probe

Successful probe in HALF_OPEN state should close the circuit.

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","circuit_state":"HALF_OPEN","probe_result":"success"}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "circuit_state": "CLOSED"}}
```

## 参考资料

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)：Martin Fowler's explanation of the circuit breaker pattern

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
