# Implement Circuit Breaking in Service Mesh

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-4-circuit-breaking>

Track: 28. The Orchestrator
Task order: 9
Short title: Circuit Breaking
Difficulty: advanced
Subtrack: Service Mesh

## Problem

When a downstream service is failing, continuing to call it wastes resources and slows down your service. A circuit breaker detects this and **fails fast**: instead of waiting for a timeout, it immediately returns an error and periodically tests whether the service has recovered.

The circuit breaker has three states:

```
CLOSED  --(failure threshold exceeded)--> OPEN
OPEN    --(after timeout)--> HALF-OPEN
HALF-OPEN --(success)--> CLOSED
HALF-OPEN --(failure)--> OPEN
```

Implement a node that enforces this state machine per service:

```json
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

## Concepts

- circuit breaker
- fail fast
- half-open state
- cascading failures
- service resilience

## Hints

- Three states: closed (calls pass through), open (fail immediately), half-open (test one call)
- Transition to open when consecutive failures >= threshold
- In half-open, allow one call through; close on success, re-open on failure
- Fail fast: when open, return error immediately without calling the downstream service
- Track failures per service so each service has its own independent circuit breaker

## Test Cases

### 1. Circuit breaker opens after failures

Circuit breaker should open after 5 consecutive failures.

Input:

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"force_failures":5}}
```

Expected output:

```text
{"type": "circuit_breaker_open", "in_reply_to": 1, "service": "service-b", "failures": 5}
```

### 2. Circuit breaker recovers on success

Successful probe in half-open state should close the breaker.

Input:

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"state":"half_open","force_success":true}}
```

Expected output:

```text
{"type": "circuit_breaker_closed", "in_reply_to": 1, "service": "service-b", "state": "closed"}
```

## Resources

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html): Martin Fowler's explanation of the circuit breaker pattern

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
