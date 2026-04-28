# 在 Saga 中实现幂等性

英文标题：Implement Idempotency in Sagas
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-4-idempotency>

课程：9. 协调器：分布式事务
任务序号：14
短标题：Saga Idempotency
难度：进阶
子主题：Saga Pattern

## 中文导读

本题要求你在 Saga 中实现幂等性（Idempotency）。在分布式系统中，网络超时等原因会导致消息被重试。如果操作不具备幂等性，重试可能会造成重复扣款等严重问题。通过这道题，你将学习如何用幂等键来确保同一操作即使被多次执行，结果也只生效一次。

## 题目说明

幂等性确保 Saga 步骤被重试时不会产生重复操作，比如重复扣款。

**幂等键**：

每个 Saga 步骤都会打上以下标签：
- saga_id: "saga42"
- step_id: 2
- idempotency_key: "saga42:step2"

**服务端的幂等性追踪**：

```typescript
processed_steps = new Map<string, PaymentResult>();

chargePayment(saga_id: string, step: number, params: ChargeParams) {
  const key = `${saga_id}:step${step}`;

  // Check if already processed
  if (this.processed_steps.has(key)) {
    console.log(`Already processed ${key}, returning cached result`);
    return this.processed_steps.get(key);
  }

  // Process and cache result
  const result = this.doCharge(params);
  this.processed_steps.set(key, result);
  return result;
}
```

**示例：重试时不会重复扣款**：

```json
// First attempt:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}
Response: {"type": "ChargePayment_ok", "saga_id": "saga42", "step": 2, "result": {"payment_id": "p1", "charged": 99.99}}

// Network timeout, orchestrator retries:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}
Response: {"type": "ChargePayment_ok", "saga_id": "saga42", "step": 2, "result": {"payment_id": "p1", "charged": 99.99}, "note": "cached_result"}

// User is only charged once (payment_id = "p1")
```

**补偿事务也必须是幂等的**：

```json
// First compensation:
{"type": "RefundPayment", "saga_id": "saga42", "step": 2, "compensating": true, "params": {"payment_id": "p1", "amount": 99.99}}
Response: {"type": "RefundPayment_ok", "saga_id": "saga42", "step": 2, "result": {"refund_id": "r1", "refunded": 99.99}}

// Retry:
{"type": "RefundPayment", "saga_id": "saga42", "step": 2, "compensating": true, "params": {"payment_id": "p1", "amount": 99.99}}
Response: {"type": "RefundPayment_ok", "saga_id": "saga42", "step": 2, "result": {"refund_id": "r1", "refunded": 99.99}, "note": "already_refunded"}
```

## 涉及概念

- `idempotency`
- `deduplication`
- `exactly-once semantics`
- `message retries`
- `saga_id + step_id`

## 实现提示

- 为每个步骤打上唯一的 saga_id + step_id 组合标签
- 服务端追踪已处理的步骤，避免重复执行
- 如果同一步骤被重试，服务应返回与之前相同的结果
- 使用幂等键：服务先检查该步骤是否已经处理过
- 例如：ChargePayment(saga42, step2) 即使被重试也只扣款一次

## 测试用例

### 1. 重试时扣款操作的幂等性

两次请求应返回相同的 payment_id。第二次请求应标注 "cached_result"。用户应该只被扣款一次。

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

### 2. 重试时退款操作的幂等性

两次请求应返回相同的 refund_id。第二次请求应标注 "already_refunded"。款项应该只被退还一次。

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

- [Idempotency Patterns](https://www.awsarchitectureblog.com/2017/01/12/idempotency-patterns-for-distributed-systems.html)：AWS 博客上关于幂等性模式的文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
