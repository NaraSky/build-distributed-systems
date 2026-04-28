# 实现限流

英文标题：Implement Rate Limiting
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-5-rate-limiting>

课程：14. 负载均衡器
任务序号：10
短标题：Rate Limiting
难度：进阶
子主题：七层负载均衡

## 中文导读

本题要求你实现限流（Rate Limiting）功能。限流就像高速公路的入口匝道——当车流量过大时，通过控制进入的速率来防止拥堵。在分布式系统中，限流保护后端服务不被过多请求压垮，防止恶意刷接口，同时确保所有用户公平使用资源。你将使用经典的令牌桶算法来实现。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

限流保护后端服务免受过多请求的冲击。它能防止滥用、确保公平使用，并在流量高峰期维持服务可用性。

**令牌桶算法**：
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

**限流配置**：
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

**限流示例**：
```json
// First 10 requests succeed:
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "client_ip": "1.2.3.4"}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": 9, "X-RateLimit-Limit": 10, "X-RateLimit-Reset": 1680123460}}

// 11th request is rate limited:
Request:  {"type": "http_request", "msg_id": 11, "method": "GET", "path": "/api/users", "client_ip": "1.2.3.4"}
Response: {"type": "http_response", "in_reply_to": 11, "status": 429, "error": "Rate limit exceeded", "headers": {"X-RateLimit-Remaining": 0, "Retry-After": 1}}
```

**按 API 密钥限流**：
```json
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "headers": {"X-API-Key": "key_free_tier"}, "client_ip": "1.2.3.4"}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": 0, "X-RateLimit-Limit": 1}}
```

## 涉及概念

- `rate limiting`
- `token bucket`
- `per-IP limits`
- `per-API-key limits`
- `DDoS protection`

## 实现提示

- 使用令牌桶算法：以固定速率补充令牌，每个请求消耗一个令牌
- 按 IP 地址和 API 密钥分别跟踪限流状态
- 当令牌桶为空时返回 429 Too Many Requests
- 在响应头中包含限流信息：X-RateLimit-Remaining、X-RateLimit-Reset
- 支持突发流量容忍：允许短时间内超过持续速率的突发请求

## 测试用例

### 1. 执行按 IP 限流

前 10 个请求应成功（状态码 200），第 11 个请求应返回 429 Too Many Requests。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"init","msg_id":1,"rate_limits":{"per_ip":{"requests_per_second":10,"burst":20}}}}
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/data","client_ip":"1.2.3.4"},"send_times":11}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 响应中包含限流头

响应应包含 X-RateLimit-Remaining 和 X-RateLimit-Limit 响应头。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/data","client_ip":"1.2.3.4"}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Remaining": .*, "X-RateLimit-Limit": 10}}}
```

## 参考资料

- [Rate Limiting Algorithms](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)：关于限流策略和技术的架构指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
