# 实现 Rate Limiting

英文标题：Implement Rate Limiting
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-5-rate-limiting>

课程：14. 负载均衡器
任务序号：10
短标题：Rate Limiting
难度：intermediate
子主题：Layer 7 Load Balancing

## 中文导读

本题要求你完成 `实现 Rate Limiting`。

重点关注：`rate limiting`、`token bucket`、`per-IP limits`、`per-API-key limits`、`DDoS protection`。

建议先按提示逐步实现：Use token bucket algorithm: refill tokens at a fixed rate, consume tokens per 请求。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Rate limiting protects backend services from being overwhelmed by too many requests. It prevents abuse, ensures fair usage,和maintains service availability during traffic spikes.

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
        return true;  // Allow 请求
    }
    return false;  // Rate limited
}
```

**Rate limit configuration**:
```JSON
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
```JSON
// First 10 requests succeed:
请求:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "client_ip": "1.2.3.4"}
响应: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": 9, "X-RateLimit-Limit": 10, "X-RateLimit-Reset": 1680123460}}

// 11th 请求 is rate limited:
请求:  {"type": "http_request", "msg_id": 11, "method": "GET", "path": "/api/users", "client_ip": "1.2.3.4"}
响应: {"type": "http_response", "in_reply_to": 11, "status": 429, "error": "Rate limit exceeded", "headers": {"X-RateLimit-Remaining": 0, "重试-After": 1}}
```

**Per-API-key rate limiting**:
```JSON
请求:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "headers": {"X-API-Key": "key_free_tier"}, "client_ip": "1.2.3.4"}
响应: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": 0, "X-RateLimit-Limit": 1}}
```

## 涉及概念

- `rate limiting`
- `token bucket`
- `per-IP limits`
- `per-API-key limits`
- `DDoS protection`

## 实现提示

- Use token bucket algorithm: refill tokens at a fixed rate, consume tokens per 请求
- Track rate limits per IP address和per API key
- Return 429 Too Many Requests when bucket is empty
- Include rate limit headers: X-RateLimit-Remaining, X-RateLimit-Reset
- Burst allowance: allow short bursts above sustained rate

## 测试用例

### 1. Enforce per-IP rate limit

First 10 requests should succeed (200), 11th should fail，包含429 Too Many Requests.

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"init","msg_id":1,"rate_limits":{"per_ip":{"requests_per_second":10,"burst":20}}}}
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/data","client_ip":"1.2.3.4"},"send_times":11}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Rate limit headers included

响应 should include X-RateLimit-Remaining和X-RateLimit-Limit headers.

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/data","client_ip":"1.2.3.4"}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": .*, "X-RateLimit-Limit": 10}}}
```

## 参考资料

- [Rate Limiting Algorithms](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)：Google Cloud architecture guide on rate limiting

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
