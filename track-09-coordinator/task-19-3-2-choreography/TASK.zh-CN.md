# 实现 Choreography-Based Saga

英文标题：Implement Choreography-Based Saga
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-2-choreography>

课程：9. 协调器：分布式事务
任务序号：12
短标题：Choreography Saga
难度：advanced
子主题：Saga Pattern

## 中文导读

本题要求你完成 `实现 Choreography-Based Saga`。

重点关注：`choreography`、`event-driven architecture`、`service coordination`、`no central orchestrator`、`event publishing`。

建议先按提示逐步实现：Each service publishes events when it completes its step。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In a choreography-based saga, there is no central coordinator. Each service listens用于events和triggers the next step by publishing its own events. Coordination happens through events, not a orchestrator.

**Choreography flow**:
```
Service A (Inventory)
  → Completes T1
  → Publishes "InventoryReserved" event
  → (if 故障) Publishes "InventoryReservationFailed"

Service B (Payment)
  → Subscribes to "InventoryReserved"
  → On event, executes T2 (ChargePayment)
  → Publishes "PaymentCharged" event
  → (if 故障) Publishes "PaymentFailed" event

Service C (Shipping)
  → Subscribes to "PaymentCharged"
  → On event, executes T3 (CreateShipment)
  → Publishes "ShipmentCreated" event
  → (if 故障) Publishes "ShipmentFailed" event
```

**Event structure**:
```JSON
// Forward path events:
{"type": "InventoryReserved", "saga_id": "saga42", "reservation_id": "r1", "timestamp": 1680123456}
{"type": "PaymentCharged", "saga_id": "saga42", "payment_id": "p1", "amount": 99.99, "timestamp": 1680123457}
{"type": "ShipmentCreated", "saga_id": "saga42", "shipment_id": "s1", "timestamp": 1680123458}

// Compensating events:
{"type": "PaymentFailed", "saga_id": "saga42", "reason": "insufficient_funds", "timestamp": 1680123457}
{"type": "InventoryReleased", "saga_id": "saga42", "reservation_id": "r1", "timestamp": 1680123458}
```

**Example choreography execution**:
```JSON
// 客户端 starts saga by calling InventoryService:
请求:  {"type": "reserve_inventory", "msg_id": 1, "saga_id": "saga42", "sku": "abc123", "quantity": 1}
响应: {"type": "reserve_inventory_ok", "in_reply_to": 1, "saga_id": "saga42", "reservation_id": "r1"}

// InventoryService publishes event, PaymentService picks it up:
{"type": "InventoryReserved", "saga_id": "saga42", "reservation_id": "r1"}

// PaymentService charges和publishes event:
{"type": "PaymentCharged", "saga_id": "saga42", "payment_id": "p1", "amount": 99.99}

// ShippingService creates shipment和publishes event:
{"type": "ShipmentCreated", "saga_id": "saga42", "shipment_id": "s1"}
```

**Handling failures in choreography**:
```JSON
// If payment fails:
{"type": "PaymentFailed", "saga_id": "saga42", "reason": "insufficient_funds"}

// InventoryService subscribes to PaymentFailed和runs compensator:
{"type": "InventoryReleased", "saga_id": "saga42", "reservation_id": "r1"}
```

## 涉及概念

- `choreography`
- `event-driven architecture`
- `service coordination`
- `no central orchestrator`
- `event publishing`

## 实现提示

- Each service publishes events when it completes its step
- The next service subscribes to those events和reacts
- No central coordinator: services communicate via events only
- Example: InventoryService publishes "InventoryReserved", PaymentService subscribes和charges
- Use a 消息 broker or event bus to 广播 events

## 测试用例

### 1. Choreography completes successfully

Choreography should complete: inventory → payment → shipping events should fire in sequence.

输入：

```json
{"src":"c0","dest":"event_bus","body":{"type":"init","msg_id":1,"services":["inventory","payment","shipping"]}}
{"src":"c1","dest":"inventory","body":{"type":"reserve_inventory","msg_id":2,"saga_id":"saga42","sku":"abc123","quantity":1}}
```

期望输出：

```text
{"src": "event_bus", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Choreography handles payment failure

When payment fails, InventoryReleased event should fire to compensate the reservation.

输入：

```json
{"src":"c0","dest":"event_bus","body":{"type":"init","msg_id":1,"services":["inventory","payment","shipping"]}}
{"src":"c1","dest":"inventory","body":{"type":"reserve_inventory","msg_id":2,"saga_id":"saga43","sku":"abc123","quantity":1,"fail_payment":true}}
```

期望输出：

```text
{"src": "event_bus", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Choreography vs Orchestration](https://www.nginx.com/blog/nginx-microservices-reference-architecture-nginxa-microservices-reference-architecture-part3-choreography-vs-orchestration/)：Comparison of choreography和orchestration patterns

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
