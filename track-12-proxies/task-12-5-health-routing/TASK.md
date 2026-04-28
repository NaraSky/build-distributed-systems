# Add Health-Based Routing

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-5-health-routing>

Track: 12. Proxies
Task order: 5
Short title: Health Routing
Difficulty: intermediate
Subtrack: Caching Proxy

## Problem

Add health-based routing with circuit breaker pattern:

1. Maintain list of backend servers
2. Periodically health-check each backend
3. Track consecutive failures per backend
4. Open circuit after N failures (stop sending traffic)
5. Periodically test with single request (half-open)
6. Close circuit on success (resume normal traffic)

This improves reliability by routing away from failing backends.

## Concept Notes

### Health Checks

Active health checks periodically probe backends with test requests. Passive checks observe real request failures. Both inform routing decisions for fast failure detection.

### Circuit Breaker

The circuit breaker prevents cascading failures. After enough failures, the circuit "opens" and requests fail immediately without trying the backend. After a timeout, one test request checks recovery (half-open state).

## Concepts

- health checks
- circuit breaker
- failover

## Hints

- Periodically check backend health
- Track failure counts per backend
- Implement circuit breaker pattern

## Test Cases

### 1. Route to healthy

Proxy has 3 backends: b1 (healthy), b2 (unhealthy, 5 failures), b3 (healthy). Health check marks b2 as down. Verify proxy only routes requests to b1 and b3, skipping unhealthy b2.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Open circuit on failures

Backend b1 initially healthy. Send requests that fail 5 times consecutively (threshold=3). After 3 failures, circuit should open for b1. Verify proxy stops sending traffic to b1 until circuit half-opens for health check.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html): Martin Fowler on circuit breakers

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
