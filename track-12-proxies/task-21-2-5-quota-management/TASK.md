# Implement Rate Limiting and Quota Management

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-5-quota-management>

Track: 12. Proxies
Task order: 10
Short title: Rate Limiting and Quotas
Difficulty: intermediate
Subtrack: API Gateway

## Problem

**Rate limiting tiers**:. ```. Free tier:. - 100 requests/hour. - 1000 requests/day. - Return 429 when exceeded. Paid tier:. - 10,000 requests/hour. - 100,000 requests/day. - Auto-scale capacity. Enterprise tier:. - Custom limits. - Burstable capacity. - Priority routing. ```. **Quota tracking**:. ```typescript. api_key: string,. tier: string,. hourly_limit: number,. daily_limit: number,. hourly_used: number,. daily_used: number,. hourly_reset: timestamp,. daily_reset: timestamp. const quota = this.quotas.get(apiKey);. const now = Date.now();. // Reset counters if period expired. quota.daily_used = 0;. quota.daily_reset = startOfDay(now + 1 day);. quota.hourly_used = 0;. quota.hourly_reset = startOfHour(now + 1 hour);. // Check limits. // Increment counters. quota.hourly_used++;. quota.daily_used++;. ```. **Example rate limiting**:. ```json. // Free tier request (within quota):. // Free tier request (quota exceeded):. // Paid tier request (higher quota):. ```

## Concepts

- rate limiting
- quota management
- API tiers
- throttling
- usage tracking
- billing integration

## Hints

- Enforce per-API-key rate limits: free tier (100 req/hour), paid tier (10000 req/hour)
- Track usage for billing: count requests per API key per billing period
- Return rate limit headers: X-RateLimit-Remaining, X-RateLimit-Reset
- Support quota override for enterprise clients
- Distinguish between soft limits (throttle) and hard limits (block)

## Test Cases

### 1. Enforce free tier quota

Should return 429 Too Many Requests with hourly limit exceeded error.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"tiers":{"free":{"hourly_limit":100,"daily_limit":1000},"paid":{"hourly_limit":10000,"daily_limit":100000}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/data","headers":{"X-API-Key":"free_key_123"},"hourly_used":100}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Rate limit headers included

Response should include X-RateLimit headers with remaining quota.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/data","headers":{"X-API-Key":"free_key_123"}}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Limit": "100", "X-RateLimit-Remaining": .*, "X-RateLimit-Reset": .*}}}
```

## Resources

- [API Gateway Rate Limiting](https://cloud.google.com/apigateway/docs/configuring-api-keys#setting_quota): Google Cloud documentation on API gateway quota management

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
