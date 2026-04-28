# Simulate Thundering Herd with Circuit Breaking

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-5-thundering-herd>

Track: 14. Load Balancers
Task order: 15
Short title: Thundering Herd
Difficulty: advanced
Subtrack: Advanced Balancing Algorithms

## Problem

The thundering herd problem occurs when a large number of clients simultaneously retry after a backend failure, overwhelming the remaining backends and causing cascading failures.

**The problem**:
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

**Circuit breaking + exponential backoff**:
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

**Example thundering herd simulation**:
```json
Request:  {"type": "simulate_thundering_herd", "msg_id": 1, "backends": ["b1", "b2", "b3", "b4"], "requests_per_second": 4000, "fail_backend": "b4", "duration_ms": 10000, "with_circuit_breaker": false}
Response: {"type": "simulation_complete", "in_reply_to": 1, "results": {"without_circuit_breaker": {"cascading_failures": true, "backends_down": ["b1", "b2", "b3"], "p99_latency_ms": 5000, "error_rate": 1.0}}}

Request:  {"type": "simulate_thundering_herd", "msg_id": 2, "backends": ["b1", "b2", "b3", "b4"], "requests_per_second": 4000, "fail_backend": "b4", "duration_ms": 10000, "with_circuit_breaker": true, "with_exponential_backoff": true}
Response: {"type": "simulation_complete", "in_reply_to": 2, "results": {"with_protections": {"cascading_failures": false, "backends_down": ["b4"], "p99_latency_ms": 150, "error_rate": 0.25}}}
```

**Metrics to track**:
- Requests per second (per backend)
- Error rate (5xx responses)
- Latency percentiles (p50, p99, p99.9)
- Circuit breaker state transitions
- Retry attempt distribution

## Concepts

- thundering herd
- cascading failures
- exponential backoff
- graceful degradation
- circuit breaking

## Hints

- Simulate: backend-4 fails, 10,000 connections suddenly redistribute to remaining backends
- Without circuit breaking: remaining backends overload and fail
- With circuit breaking: failed backend is removed from pool immediately
- With exponential backoff: clients retry with increasing delays
- Measure: requests/sec, error rate, latency p99 before and after failure

## Test Cases

### 1. Thundering herd without protections

Without circuit breaking, thundering herd should cause all backends to fail (cascading failure).

Input:

```json
{"src":"client","dest":"simulator","body":{"type":"simulate_thundering_herd","msg_id":1,"backends":["b1","b2","b3","b4"],"requests_per_second":4000,"fail_backend":"b4","with_circuit_breaker":false}}
```

Expected output:

```text
{"src": "simulator", "dest": "client", "body": {"type": "simulation_complete", "in_reply_to": 1, "results": {"cascading_failures": true, "all_backends_failed": true, "error_rate": 1.0}}}
```

### 2. Circuit breaking prevents cascade

With circuit breaking, only b4 should fail. b1, b2, b3 should stay healthy.

Input:

```json
{"src":"client","dest":"simulator","body":{"type":"simulate_thundering_herd","msg_id":1,"backends":["b1","b2","b3","b4"],"requests_per_second":4000,"fail_backend":"b4","with_circuit_breaker":true}}
```

Expected output:

```text
{"src": "simulator", "dest": "client", "body": {"type": "simulation_complete", "in_reply_to": 1, "results": {"cascading_failures": false, "failed_backends": ["b4"], "error_rate": 0.25}}}
```

## Resources

- [Thundering Herd Problem](https://www.awsarchitectureblog.com/2015/03/05/thundering-herds.html): AWS blog on thundering herd and mitigation strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
