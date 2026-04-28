# Implement Idempotency in Sagas

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-4-idempotency>

Track: 9. The Coordinator
Task order: 14
Short title: Saga Idempotency
Difficulty: intermediate
Subtrack: Saga Pattern

## Problem

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
    console.log(`Already processed ${key}, returning cached result`);
    return this.processed_steps.get(key);
  }

  // Process and cache result
  const result = this.doCharge(params);
  this.processed_steps.set(key, result);
  return result;
}
```

**Example: Retry without double-charge**:

```json
// First attempt:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}
Response: {"type": "ChargePayment_ok", "saga_id": "saga42", "step": 2, "result": {"payment_id": "p1", "charged": 99.99}}

// Network timeout, orchestrator retries:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}
Response: {"type": "ChargePayment_ok", "saga_id": "saga42", "step": 2, "result": {"payment_id": "p1", "charged": 99.99}, "note": "cached_result"}

// User is only charged once (payment_id = "p1")
```

**Compensating transactions must also be idempotent**:

```json
// First compensation:
{"type": "RefundPayment", "saga_id": "saga42", "step": 2, "compensating": true, "params": {"payment_id": "p1", "amount": 99.99}}
Response: {"type": "RefundPayment_ok", "saga_id": "saga42", "step": 2, "result": {"refund_id": "r1", "refunded": 99.99}}

// Retry:
{"type": "RefundPayment", "saga_id": "saga42", "step": 2, "compensating": true, "params": {"payment_id": "p1", "amount": 99.99}}
Response: {"type": "RefundPayment_ok", "saga_id": "saga42", "step": 2, "result": {"refund_id": "r1", "refunded": 99.99}, "note": "already_refunded"}
```

## Concepts

- idempotency
- deduplication
- exactly-once semantics
- message retries
- saga_id + step_id

## Hints

- Tag each step with a unique saga_id + step_id combination
- Services track processed steps to avoid duplicate work
- If a step is retried, the service should return the same result
- Use idempotency keys: the service checks if it already processed this step
- Example: ChargePayment(saga42, step2) should only charge once, even if retried

## Test Cases

### 1. Idempotent charge on retry

Both requests should return the same payment_id. Second request should note "cached_result". User should only be charged once.

Input:

```json
{"src":"c0","dest":"payment","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"payment","body":{"type":"ChargePayment","msg_id":2,"saga_id":"saga42","step":2,"params":{"user_id":"u42","amount":99.99}}}
{"src":"c1","dest":"payment","body":{"type":"ChargePayment","msg_id":3,"saga_id":"saga42","step":2,"params":{"user_id":"u42","amount":99.99}}}
```

Expected output:

```text
{"src": "payment", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Idempotent refund on retry

Both requests should return the same refund_id. Second request should note "already_refunded". Payment should only be refunded once.

Input:

```json
{"src":"c0","dest":"payment","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"payment","body":{"type":"RefundPayment","msg_id":2,"saga_id":"saga42","step":2,"params":{"payment_id":"p1","amount":99.99}}}
{"src":"c1","dest":"payment","body":{"type":"RefundPayment","msg_id":3,"saga_id":"saga42","step":2,"params":{"payment_id":"p1","amount":99.99}}}
```

Expected output:

```text
{"src": "payment", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Idempotency Patterns](https://www.awsarchitectureblog.com/2017/01/12/idempotency-patterns-for-distributed-systems.html): AWS blog on idempotency patterns

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
