# Implement Rate Limiting

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-5-rate-limiting>

Track: 14. Load Balancers
Task order: 10
Short title: Rate Limiting
Difficulty: intermediate
Subtrack: Layer 7 Load Balancing

## Problem

Rate limiting protects backend services from being overwhelmed by too many requests. It prevents abuse, ensures fair usage, and maintains service availability during traffic spikes.

**Token bucket algorithm**:
```
bucket: {
    tokens: number,           // Current tokens (max: capacity)
    capacity: number,         // Max tokens (burst allowance)
    refillRate: number,       // Tokens added per second
    lastRefill: timestamp     // Last refill time
}

function allowRequest(): boolean {
    now = currentTime();
    elapsed = now - bucket.lastRefill;
    bucket.tokens += elapsed * bucket.refillRate;
    bucket.tokens = min(bucket.tokens, bucket.capacity);
    bucket.lastRefill = now;

    if (bucket.tokens >= 1) {
        bucket.tokens -= 1;
        return true;  // Allow request
    }
    return false;  // Rate limited
}
```

**Rate limit configuration**:
```json
{
  "rate_limits": {
    "per_ip": {
      "requests_per_second": 10,
      "burst": 20
    },
    "per_api_key": {
      "free_tier": {"requests_per_second": 1, "burst": 5},
      "paid_tier": {"requests_per_second": 100, "burst": 200}
    }
  }
}
```

**Example rate limiting**:
```json
// First 10 requests succeed:
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "client_ip": "1.2.3.4"}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": 9, "X-RateLimit-Limit": 10, "X-RateLimit-Reset": 1680123460}}

// 11th request is rate limited:
Request:  {"type": "http_request", "msg_id": 11, "method": "GET", "path": "/api/users", "client_ip": "1.2.3.4"}
Response: {"type": "http_response", "in_reply_to": 11, "status": 429, "error": "Rate limit exceeded", "headers": {"X-RateLimit-Remaining": 0, "Retry-After": 1}}
```

**Per-API-key rate limiting**:
```json
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "headers": {"X-API-Key": "key_free_tier"}, "client_ip": "1.2.3.4"}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": 0, "X-RateLimit-Limit": 1}}
```

## Concepts

- rate limiting
- token bucket
- per-IP limits
- per-API-key limits
- DDoS protection

## Hints

- Use token bucket algorithm: refill tokens at a fixed rate, consume tokens per request
- Track rate limits per IP address and per API key
- Return 429 Too Many Requests when bucket is empty
- Include rate limit headers: X-RateLimit-Remaining, X-RateLimit-Reset
- Burst allowance: allow short bursts above sustained rate

## Test Cases

### 1. Enforce per-IP rate limit

First 10 requests should succeed (200), 11th should fail with 429 Too Many Requests.

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"init","msg_id":1,"rate_limits":{"per_ip":{"requests_per_second":10,"burst":20}}}}
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/data","client_ip":"1.2.3.4"},"send_times":11}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Rate limit headers included

Response should include X-RateLimit-Remaining and X-RateLimit-Limit headers.

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/data","client_ip":"1.2.3.4"}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": .*, "X-RateLimit-Limit": 10}}}
```

## Resources

- [Rate Limiting Algorithms](https://cloud.google.com/architecture/rate-limiting-strategies-techniques): Google Cloud architecture guide on rate limiting

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
