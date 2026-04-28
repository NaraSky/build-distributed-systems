# 实现 Rate Limiting和Quota Management

英文标题：Implement Rate Limiting和Quota Management
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-5-quota-management>

课程：12. 代理
任务序号：10
短标题：Rate Limiting和Quotas
难度：intermediate
子主题：API Gateway

## 中文导读

本题要求你完成 `实现 Rate Limiting和Quota Management`。

重点关注：`rate limiting`、`quota management`、`API tiers`、`throttling`、`usage tracking`。

建议先按提示逐步实现：Enforce per-API-key rate limits: free tier (100 req/hour), paid tier (10000 req/hour)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

**Rate limiting tiers**:. ```. Free tier:. - 100 requests/hour. - 1000 requests/day. - Return 429 when exceeded. Paid tier:. - 10,000 requests/hour. - 100,000 requests/day. - Auto-scale capacity. Enterprise tier:. - Custom limits. - Burstable capacity. - Priority routing. ```. **Quota tracking**:. ```typescript. api_key: string,. tier: string,. hourly_limit: number,. daily_limit: number,. hourly_used: number,. daily_used: number,. hourly_reset: timestamp,. daily_reset: timestamp. const quota = this.quotas.get(apiKey);. const now = Date.now();. // Reset counters if period expired. quota.daily_used = 0;. quota.daily_reset = startOfDay(now + 1 day);. quota.hourly_used = 0;. quota.hourly_reset = startOfHour(now + 1 hour);. // Check limits. // Increment counters. quota.hourly_used++;. quota.daily_used++;. ```. **Example rate limiting**:. ```JSON. // Free tier 请求 (within quota):. // Free tier 请求 (quota exceeded):. // Paid tier 请求 (higher quota):. ```

## 涉及概念

- `rate limiting`
- `quota management`
- `API tiers`
- `throttling`
- `usage tracking`
- `billing integration`

## 实现提示

- Enforce per-API-key rate limits: free tier (100 req/hour), paid tier (10000 req/hour)
- Track usage用于billing: count requests per API key per billing period
- Return rate limit headers: X-RateLimit-Remaining, X-RateLimit-Reset
- Support quota override用于enterprise clients
- Distinguish between soft limits (throttle)和hard limits (block)

## 测试用例

### 1. Enforce free tier quota

Should return 429 Too Many Requests，包含hourly limit exceeded error.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"tiers":{"free":{"hourly_limit":100,"daily_limit":1000},"paid":{"hourly_limit":10000,"daily_limit":100000}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/data","headers":{"X-API-Key":"free_key_123"},"hourly_used":100}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Rate limit headers included

响应 should include X-RateLimit headers，包含remaining quota.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/data","headers":{"X-API-Key":"free_key_123"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Limit": "100", "X-RateLimit-Remaining": .*, "X-RateLimit-Reset": .*}}}
```

## 参考资料

- [API Gateway Rate Limiting](https://cloud.google.com/apigateway/docs/configuring-api-keys#setting_quota)：Google Cloud documentation on API gateway quota management

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
