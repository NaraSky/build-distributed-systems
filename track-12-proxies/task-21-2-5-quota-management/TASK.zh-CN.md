# 实现限流与配额管理

英文标题：Implement Rate Limiting and Quota Management
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-5-quota-management>

课程：12. 代理
任务序号：10
短标题：限流与配额
难度：进阶
子主题：API 网关

## 中文导读

这道题要求你在 API 网关中实现限流（Rate Limiting）和配额管理（Quota Management）。限流是保护后端服务的重要手段，通过限制每个客户端在单位时间内的请求次数，防止某个客户端占用过多资源。配额管理则进一步按照不同的用户等级设置不同的限制，是 API 商业化运营的基础能力。

## 题目说明

**限流等级**：
```
免费等级：
  - 每小时 100 个请求
  - 每天 1000 个请求
  - 超出后返回 429 状态码

付费等级：
  - 每小时 10,000 个请求
  - 每天 100,000 个请求
  - 自动扩容

企业等级：
  - 自定义限制
  - 可突发容量
  - 优先路由
```

**配额跟踪**：
```typescript
api_key: string,
tier: string,
hourly_limit: number,
daily_limit: number,
hourly_used: number,
daily_used: number,
hourly_reset: timestamp,
daily_reset: timestamp

const quota = this.quotas.get(apiKey);
const now = Date.now();

// 如果计数周期已过，重置计数器
quota.daily_used = 0;
quota.daily_reset = startOfDay(now + 1 day);
quota.hourly_used = 0;
quota.hourly_reset = startOfHour(now + 1 hour);

// 检查是否超出限制
// 递增计数器
quota.hourly_used++;
quota.daily_used++;
```

**限流示例**：
```json
// 免费等级请求（配额内）：正常返回
// 免费等级请求（配额已用完）：返回 429
// 付费等级请求（更高配额）：正常返回
```

## 涉及概念

- `rate limiting`
- `quota management`
- `API tiers`
- `throttling`
- `usage tracking`
- `billing integration`

## 实现提示

- 按 API 密钥实施限流：免费等级每小时 100 个请求，付费等级每小时 10000 个请求
- 跟踪使用量以便计费：按 API 密钥和计费周期统计请求次数
- 在响应中返回限流相关头部：X-RateLimit-Remaining（剩余额度）、X-RateLimit-Reset（重置时间）
- 支持企业客户的配额覆盖
- 区分软限制（降速）和硬限制（拒绝）

## 测试用例

### 1. 执行免费等级配额

超出配额时应返回 429 Too Many Requests，提示每小时限额已用完。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"tiers":{"free":{"hourly_limit":100,"daily_limit":1000},"paid":{"hourly_limit":10000,"daily_limit":100000}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/data","headers":{"X-API-Key":"free_key_123"},"hourly_used":100}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 包含限流头部

响应中应包含 X-RateLimit 头部，显示剩余配额信息。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/data","headers":{"X-API-Key":"free_key_123"}}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 200, "headers": {"X-RateLimit-Limit": "100", "X-RateLimit-Remaining": .*, "X-RateLimit-Reset": .*}}}
```

## 参考资料

- [API Gateway Rate Limiting](https://cloud.google.com/apigateway/docs/configuring-api-keys#setting_quota)：Google Cloud 关于 API 网关配额管理的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
