# 实现 Idempotency in Sagas

英文标题：Implement Idempotency in Sagas
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-4-idempotency>

课程：9. 协调器：分布式事务
任务序号：14
短标题：Saga Idempotency
难度：intermediate
子主题：Saga Pattern

## 中文导读

本题要求你完成 `实现 Idempotency in Sagas`。

重点关注：`idempotency`、`deduplication`、`exactly-once semantics`、`message retries`、`saga_id + step_id`。

建议先按提示逐步实现：Tag each step，包含a unique saga_id + step_id combination。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Idempotency ensures that retrying saga steps doesn't cause duplicate operations like double-charging payments.

**Idempotency key**:

Each saga step is tagged with:
- saga_id: "saga42"
- step_id: 2
- idempotency_key: "saga42:step2"

**Service-side idempotency tracking**:

```typescript
processed_steps = new Map<string, PaymentResult>();

chargePayment(saga_id: string, step: number, params: ChargeParams) {
  const key = `${saga_id}:step${step}`;

  // Check if already processed
  if (this.processed_steps.has(key)) {
    console.日志(`Already processed ${key}, returning cached result`);
    return this.processed_steps.get(key);
  }

  // Process和缓存 result
  const result = this.doCharge(params);
  this.processed_steps.set(key, result);
  return result;
}
```

**Example: 重试 without double-charge**:

```JSON
// First attempt:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}
响应: {"type": "ChargePayment_ok", "saga_id": "saga42", "step": 2, "result": {"payment_id": "p1", "charged": 99.99}}

// 网络 超时, orchestrator retries:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}
响应: {"type": "ChargePayment_ok", "saga_id": "saga42", "step": 2, "result": {"payment_id": "p1", "charged": 99.99}, "note": "cached_result"}

// User is only charged once (payment_id = "p1")
```

**Compensating transactions must also be idempotent**:

```JSON
// First compensation:
{"type": "RefundPayment", "saga_id": "saga42", "step": 2, "compensating": true, "params": {"payment_id": "p1", "amount": 99.99}}
响应: {"type": "RefundPayment_ok", "saga_id": "saga42", "step": 2, "result": {"refund_id": "r1", "refunded": 99.99}}

// 重试:
{"type": "RefundPayment", "saga_id": "saga42", "step": 2, "compensating": true, "params": {"payment_id": "p1", "amount": 99.99}}
响应: {"type": "RefundPayment_ok", "saga_id": "saga42", "step": 2, "result": {"refund_id": "r1", "refunded": 99.99}, "note": "already_refunded"}
```

## 涉及概念

- `idempotency`
- `deduplication`
- `exactly-once semantics`
- `message retries`
- `saga_id + step_id`

## 实现提示

- Tag each step，包含a unique saga_id + step_id combination
- Services track processed steps to avoid duplicate work
- If a step is retried, the service should return the same result
- Use idempotency keys: the service checks if it already processed this step
- Example: ChargePayment(saga42, step2) should only charge once, even if retried

## 测试用例

### 1. Idempotent charge on 重试

Both requests should return the same payment_id. Second 请求 should note "cached_result". User should only be charged once.

输入：

```json
{"src":"c0","dest":"payment","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"payment","body":{"type":"ChargePayment","msg_id":2,"saga_id":"saga42","step":2,"params":{"user_id":"u42","amount":99.99}}}
{"src":"c1","dest":"payment","body":{"type":"ChargePayment","msg_id":3,"saga_id":"saga42","step":2,"params":{"user_id":"u42","amount":99.99}}}
```

期望输出：

```text
{"src": "payment", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Idempotent refund on 重试

Both requests should return the same refund_id. Second 请求 should note "already_refunded". Payment should only be refunded once.

输入：

```json
{"src":"c0","dest":"payment","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"payment","body":{"type":"RefundPayment","msg_id":2,"saga_id":"saga42","step":2,"params":{"payment_id":"p1","amount":99.99}}}
{"src":"c1","dest":"payment","body":{"type":"RefundPayment","msg_id":3,"saga_id":"saga42","step":2,"params":{"payment_id":"p1","amount":99.99}}}
```

期望输出：

```text
{"src": "payment", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Idempotency Patterns](https://www.awsarchitectureblog.com/2017/01/12/idempotency-patterns-for-distributed-systems.html)：AWS blog on idempotency patterns

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
