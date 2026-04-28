# Implement Circuit Breaking

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-4-circuit-breaking>

Track: 14. Load Balancers
Task order: 9
Short title: Circuit Breaking
Difficulty: advanced
Subtrack: Layer 7 Load Balancing

## Problem

**Circuit states**:. ```. CLOSED (normal). - Requests pass through to backend. - Track failures in a sliding window. - If failures > threshold → OPEN. OPEN (failing). - All requests fail fast (no backend attempts). - After timeout → HALF_OPEN. HALF_OPEN (testing). - Allow one probe request through. - If success → CLOSED. - If failure → OPEN. ```. **Failure tracking**:. ```typescript. state: "CLOSED" | "OPEN" | "HALF_OPEN";. failureCount: number;. lastFailureTime: number;. successCount: number;. // Configuration. failureThreshold: number = 5; // Open after 5 failures. timeout: number = 60000; // Try again after 60s. halfOpenMaxAttempts: number = 1; // One probe request. ```. **Example circuit breaking**:. ```json. // Backend is healthy (circuit closed):. // Backend starts failing (5 failures in 30s):. // After 60s timeout (half-open):. ```. **Circuit breaker metrics**:. ```json. "backend": "api-1",. "state": "OPEN",. "failure_count": 7,. "last_failure_time": 1680123456,. "opened_at": 1680123450,. "next_attempt_at": 1680123510. ```

## Concepts

- circuit breaker
- failure threshold
- half-open state
- automatic recovery
- cascade prevention

## Hints

- Track failures per backend: if failure_count > threshold (e.g., 5), open circuit
- Open circuit: reject requests immediately without trying backend
- After timeout (e.g., 60s), enter half-open state: send one probe request
- If probe succeeds, close circuit; if fails, reopen circuit
- This prevents cascading failures when a backend is overwhelmed

## Test Cases

### 1. Circuit opens after threshold failures

After 5 failures, circuit should open and return 503 without attempting backend.

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","simulate_failures":5}}
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/users"}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 500, "backend": "api-1"}}
```

### 2. Circuit closes after successful probe

Successful probe in HALF_OPEN state should close the circuit.

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","circuit_state":"HALF_OPEN","probe_result":"success"}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "circuit_state": "CLOSED"}}
```

## Resources

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html): Martin Fowler's explanation of the circuit breaker pattern

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
