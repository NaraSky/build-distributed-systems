# 实现电商结账 Saga

英文标题：Implement E-Commerce Checkout Saga
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-5-shopping-cart>

课程：9. 协调器：分布式事务
任务序号：15
短标题：E-Commerce Saga
难度：高级
子主题：Saga Pattern

## 中文导读

本题要求你实现一个完整的电商结账 Saga，涵盖库存、支付和物流三个服务。这是一个贴近真实业务场景的综合练习，帮助你把前面学到的 Saga 模式知识应用到实际的电商下单流程中。

## 题目说明

实现一个完整的电商结账 Saga，包含库存服务、支付服务和物流服务。这个练习展示了 Saga 模式在真实业务场景中的应用。

**电商结账 Saga 流程**：
```
第 1 步：预留库存（ReserveInventory）
  - 服务：库存服务
  - 操作：预留商品数量
  - 补偿操作：释放库存（ReleaseReservation）

第 2 步：扣款（ChargePayment）
  - 服务：支付服务
  - 操作：对信用卡扣款
  - 补偿操作：退款（RefundPayment）

第 3 步：创建物流（CreateShipment）
  - 服务：物流服务
  - 操作：生成物流单
  - 补偿操作：取消物流（CancelShipment）
```

**正常路径示例**：
```json
Request:  {"type": "checkout", "msg_id": 1, "saga_id": "checkout42", "user_id": "u42", "items": [{"sku": "abc123", "quantity": 2}, {"sku": "xyz789", "quantity": 1}], "shipping_address": "123 Main St"}

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

**失败路径示例**：
```json
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

- 完整建模电商结账流程，包含三个步骤
- T1：预留库存，将商品从可售库存中预留出来
- T2：扣款，对用户的信用卡进行扣费
- T3：创建物流，生成物流单和快递单号
- 对应的补偿操作：释放库存、退款、取消物流

## 测试用例

### 1. 成功结账

checkout_complete 应包含 status=COMPLETED，以及 order_id、payment_id 和 shipment_id。

输入：

```json
{"src":"c0","dest":"checkout_orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"checkout_orchestrator","body":{"type":"checkout","msg_id":2,"saga_id":"checkout42","user_id":"u42","items":[{"sku":"abc123","quantity":2}],"shipping_address":"123 Main St"}}
```

期望输出：

```text
{"src": "checkout_orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 支付失败触发回滚

checkout_failed 应包含 status=ABORTED，库存应被释放（执行补偿操作）。

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

- [Saga Pattern for E-Commerce](https://www.awsarchitectureblog.com/2017/01/12/managing-distributed-transactions-with-saga-pattern.html)：AWS 博客上关于在电商场景中使用 Saga 模式的文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
