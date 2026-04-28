# 实现 E-Commerce Checkout Saga

英文标题：Implement E-Commerce Checkout Saga
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-5-shopping-cart>

课程：9. 协调器：分布式事务
任务序号：15
短标题：E-Commerce Saga
难度：advanced
子主题：Saga Pattern

## 中文导读

本题要求你完成 `实现 E-Commerce Checkout Saga`。

重点关注：`e-commerce saga`、`inventory reservation`、`payment processing`、`shipment creation`、`real-world saga`。

建议先按提示逐步实现：Model the complete e-commerce checkout flow，包含3 steps。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a complete e-commerce checkout saga，包含inventory, payment,和shipping services. This demonstrates the saga pattern in a realistic scenario.

**E-commerce checkout saga**:
```
Step 1: ReserveInventory
  - Service: InventoryService
  - Action: Reserve SKU quantities
  - Compensator: ReleaseReservation

Step 2: ChargePayment
  - Service: PaymentService
  - Action: Charge credit card
  - Compensator: RefundPayment

Step 3: CreateShipment
  - Service: ShippingService
  - Action: Create shipping label
  - Compensator: CancelShipment
```

**Happy path example**:
```JSON
请求:  {"type": "checkout", "msg_id": 1, "saga_id": "checkout42", "user_id": "u42", "items": [{"sku": "abc123", "quantity": 2}, {"sku": "xyz789", "quantity": 1}], "shipping_address": "123 Main St"}

// Step 1: ReserveInventory
{"type": "ReserveInventory", "saga_id": "checkout42", "step": 1, "items": [{"sku": "abc123", "quantity": 2}, {"sku": "xyz789", "quantity": 1}]}
{"type": "ReserveInventory_ok", "saga_id": "checkout42", "step": 1, "reservations": [{"sku": "abc123", "reservation_id": "r1"}, {"sku": "xyz789", "reservation_id": "r2"}]}

// Step 2: ChargePayment
{"type": "ChargePayment", "saga_id": "checkout42", "step": 2, "user_id": "u42", "amount": 249.99}
{"type": "ChargePayment_ok", "saga_id": "checkout42", "step": 2, "payment_id": "p1", "transaction_id": "txn_12345"}

// Step 3: CreateShipment
{"type": "CreateShipment", "saga_id": "checkout42", "step": 3, "items": [...], "address": "123 Main St"}
{"type": "CreateShipment_ok", "saga_id": "checkout42", "step": 3, "shipment_id": "s1", "tracking_number": "1Z999AA1"}

// Saga complete:
{"type": "checkout_complete", "saga_id": "checkout42", "status": "COMPLETED", "order_id": "o123"}
```

**故障 path example**:
```JSON
// Step 1: ReserveInventory (succeeds)
{"type": "ReserveInventory_ok", "saga_id": "checkout43", "step": 1, "reservations": [...]}

// Step 2: ChargePayment (fails - insufficient funds)
{"type": "ChargePayment_failed", "saga_id": "checkout43", "step": 2, "error": "insufficient_funds", "decline_code": "DECLINED"}

// Compensating: ReleaseReservation
{"type": "ReleaseReservation", "saga_id": "checkout43", "step": 1, "compensating": true, "reservations": [...]}
{"type": "ReleaseReservation_ok", "saga_id": "checkout43", "step": 1}

// Saga aborted:
{"type": "checkout_failed", "saga_id": "checkout43", "status": "ABORTED", "reason": "Payment declined: DECLINED"}
```

## 涉及概念

- `e-commerce saga`
- `inventory reservation`
- `payment processing`
- `shipment creation`
- `real-world saga`
- `compensating transactions`

## 实现提示

-模式l the complete e-commerce checkout flow，包含3 steps
- T1: ReserveInventory - reserve items in stock
- T2: ChargePayment - charge user's credit card
- T3: CreateShipment - create shipping label
- Compensators: ReleaseInventory, RefundPayment, CancelShipment

## 测试用例

### 1. Successful checkout

checkout_complete should have status=COMPLETED，包含order_id, payment_id,和shipment_id.

输入：

```json
{"src":"c0","dest":"checkout_orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"checkout_orchestrator","body":{"type":"checkout","msg_id":2,"saga_id":"checkout42","user_id":"u42","items":[{"sku":"abc123","quantity":2}],"shipping_address":"123 Main St"}}
```

期望输出：

```text
{"src": "checkout_orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Payment failure triggers rollback

checkout_failed should have status=ABORTED和inventory should be released (compensated).

输入：

```json
{"src":"c0","dest":"checkout_orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"checkout_orchestrator","body":{"type":"checkout","msg_id":2,"saga_id":"checkout43","user_id":"u999","items":[{"sku":"abc123","quantity":2}],"shipping_address":"123 Main St"}}
```

期望输出：

```text
{"src": "checkout_orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Saga Pattern用于E-Commerce](https://www.awsarchitectureblog.com/2017/01/12/managing-distributed-transactions-with-saga-pattern.html)：AWS blog on使用saga pattern用于e-commerce

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
