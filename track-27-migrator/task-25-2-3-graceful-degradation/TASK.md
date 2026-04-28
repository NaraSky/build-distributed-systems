# Implement Graceful API Degradation

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-3-graceful-degradation>

Track: 27. The Migrator
Task order: 8
Short title: Graceful Degradation
Difficulty: advanced
Subtrack: Protocol and API Evolution

## Problem

Graceful degradation keeps your API functional even when downstream services are failing. Instead of returning errors, you serve cached data, disable non-critical features, or queue requests for later processing. The user gets a slightly degraded experience instead of a complete outage.

Implement a node that degrades gracefully under failure conditions:

```json
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

## Concepts

- graceful degradation
- circuit breaker
- fallback cache
- feature flags
- request queuing

## Hints

- Circuit breaker: after threshold failures, return cached data instead of calling the failing service
- Cached fallback: return stale data with _cached: true when a dependency is down
- Feature flags: disable expensive non-critical features (recommendations, search) under high load
- Request queuing: accept the request and queue it for later processing when the service is down
- circuit_state: "open" means the circuit breaker is tripped and using the fallback

## Test Cases

### 1. Circuit breaker opens after failures

After 6 failures the circuit opens and serves cached data.

Input:

```json
{"src":"client","dest":"api","body":{"type":"get_user","msg_id":1,"user_id":123,"force_failures":6}}
```

Expected output:

```text
{"type": "user_response", "in_reply_to": 1, "user": {"id": 123, "name": "John Doe"}, "circuit_state": "open", "from_cache": true}
```

### 2. Fallback to cached data

Service unavailable should return stale cached data.

Input:

```json
{"src":"client","dest":"api","body":{"type":"get_product","msg_id":1,"product_id":123,"service_unavailable":true}}
```

Expected output:

```text
{"type": "product_response", "in_reply_to": 1, "product": {"id": 123, "name": "Product"}, "_cached": true}
```

## Resources

- [Graceful Degradation](https://docs.microsoft.com/en-us/azure/architecture/patterns/bulkhead): Bulkhead and circuit breaker patterns for graceful degradation
- [Graceful Degradation](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/): AWS builders library on graceful degradation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
