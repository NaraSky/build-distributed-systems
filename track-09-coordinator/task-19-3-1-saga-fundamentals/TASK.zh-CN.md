# 实现 Saga Pattern，包含Compensating Transactions

英文标题：Implement Saga Pattern，包含Compensating Transactions
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-1-saga-fundamentals>

课程：9. 协调器：分布式事务
任务序号：11
短标题：Saga Fundamentals
难度：intermediate
子主题：Saga Pattern

## 中文导读

本题要求你完成 `实现 Saga Pattern，包含Compensating Transactions`。

重点关注：`saga pattern`、`compensating transactions`、`local transactions`、`rollback`、`long-running transactions`。

建议先按提示逐步实现：A saga is a sequence of local transactions T1, T2, ..., Tn。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The Saga pattern manages long-running transactions by breaking them into a sequence of local transactions，包含compensating actions用于rollback. Unlike 2PC, each step commits immediately, but can be undone by its compensating 事务.

**Saga structure**:
```
Transactions: T1, T2, ..., Tn
Compensators: C1, C2, ..., Cn

Execution:
  T1 → T2 → T3 → ... → Tn (forward path)

If Ti fails:
  C(i-1) → C(i-2) → ... → C1 (backward path)
```

**Example e-commerce saga**:
```
T1: ReserveInventory (sku="abc123", quantity=1)
    C1: ReleaseReservation (sku="abc123", quantity=1)

T2: ChargePayment (user_id="u42", amount=99.99)
    C2: RefundPayment (user_id="u42", amount=99.99)

T3: CreateShipment (order_id="o123", address="...")
    C3: CancelShipment (order_id="o123")
```

**Forward execution (happy path)**:
```JSON
请求:  {"type": "saga_begin", "msg_id": 1, "saga_id": "saga42", "steps": [
    {"事务": "ReserveInventory", "params": {"sku": "abc123", "quantity": 1}},
    {"事务": "ChargePayment", "params": {"user_id": "u42", "amount": 99.99}},
    {"事务": "CreateShipment", "params": {"order_id": "o123"}}
]}

响应: {"type": "saga_begin_ok", "in_reply_to": 1, "saga_id": "saga42", "status": "pending"}

// Step 1 completes:
{"type": "step_complete", "saga_id": "saga42", "step": 1, "事务": "ReserveInventory", "result": "reservation_id=r1"}

// Step 2 completes:
{"type": "step_complete", "saga_id": "saga42", "step": 2, "事务": "ChargePayment", "result": "payment_id=p1"}

// Step 3 completes:
{"type": "step_complete", "saga_id": "saga42", "step": 3, "事务": "CreateShipment", "result": "shipment_id=s1"}

// Saga complete:
{"type": "saga_complete", "saga_id": "saga42", "status": "completed"}
```

**Rollback execution (故障 path)**:
```JSON
// Step 1 completes:
{"type": "step_complete", "saga_id": "saga42", "step": 1, "事务": "ReserveInventory"}

// Step 2 fails:
{"type": "step_failed", "saga_id": "saga42", "step": 2, "事务": "ChargePayment", "error": "insufficient_funds"}

// Compensating transactions run:
{"type": "compensate", "saga_id": "saga42", "step": 1, "compensator": "ReleaseReservation", "params": {"reservation_id": "r1"}}

// Saga aborted:
{"type": "saga_aborted", "saga_id": "saga42", "status": "aborted", "reason": "Step 2 failed: insufficient_funds"}
```

## 涉及概念

- `saga pattern`
- `compensating transactions`
- `local transactions`
- `rollback`
- `long-running transactions`

## 实现提示

- A saga is a sequence of local transactions T1, T2, ..., Tn
- Each 事务 Ti has a compensating 事务 Ci
- If Ti fails, run C(i-1), ..., C1 to rollback
- Each Ti commits locally (no 2PC lock-in)
- Example: ReserveInventory (T1) → ChargePayment (T2) → CreateShipment (T3)

## 测试用例

### 1. Successful saga execution

saga_begin_ok should return saga_id和the saga should complete all 3 steps successfully.

输入：

```json
{"src":"c0","dest":"saga_orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"saga_orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga42","steps":[{"transaction":"ReserveInventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","params":{"user_id":"u42","amount":50}},{"transaction":"CreateShipment","params":{"order_id":"o123"}}]}}
```

期望输出：

```text
{"src": "saga_orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Saga rollback on payment failure

When ChargePayment fails, the compensator ReleaseReservation should run和saga should be aborted.

输入：

```json
{"src":"c0","dest":"saga_orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"saga_orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga43","steps":[{"transaction":"ReserveInventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","params":{"user_id":"u999","amount":99999}},{"transaction":"CreateShipment","params":{"order_id":"o124"}}]}}
```

期望输出：

```text
{"src": "saga_orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Saga Pattern](https://microservices.io/patterns/data/saga.html)：Saga pattern documentation from microservices.io

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
