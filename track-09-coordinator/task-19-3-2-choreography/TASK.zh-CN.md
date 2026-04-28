# 实现基于编排的 Saga

英文标题：Implement Choreography-Based Saga
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-2-choreography>

课程：9. 协调器：分布式事务
任务序号：12
短标题：Choreography Saga
难度：高级
子主题：Saga Pattern

## 中文导读

本题要求你实现基于编排（Choreography）的 Saga。在这种模式下，没有集中式的协调者，各服务之间通过发布和订阅事件来协调工作。每个服务完成自己的操作后发布事件，下一个服务监听到事件后执行自己的步骤。这种去中心化的方式适合简单的流程，但随着步骤增多，协调逻辑会变得复杂。

## 题目说明

在基于编排的 Saga 中，不存在集中式协调者。每个服务监听事件，完成自己的步骤后发布新的事件来触发下一个步骤。整个协调过程通过事件驱动完成，而不依赖编排器（Orchestrator）。

**编排流程**：
```
服务 A（库存服务）
  → 完成 T1
  → 发布 "InventoryReserved" 事件
  → （如果失败）发布 "InventoryReservationFailed" 事件

服务 B（支付服务）
  → 订阅 "InventoryReserved" 事件
  → 收到事件后执行 T2（扣款）
  → 发布 "PaymentCharged" 事件
  → （如果失败）发布 "PaymentFailed" 事件

服务 C（物流服务）
  → 订阅 "PaymentCharged" 事件
  → 收到事件后执行 T3（创建物流）
  → 发布 "ShipmentCreated" 事件
  → （如果失败）发布 "ShipmentFailed" 事件
```

**事件结构**：
```json
// Forward path events:
{"type": "InventoryReserved", "saga_id": "saga42", "reservation_id": "r1", "timestamp": 1680123456}
{"type": "PaymentCharged", "saga_id": "saga42", "payment_id": "p1", "amount": 99.99, "timestamp": 1680123457}
{"type": "ShipmentCreated", "saga_id": "saga42", "shipment_id": "s1", "timestamp": 1680123458}

// Compensating events:
{"type": "PaymentFailed", "saga_id": "saga42", "reason": "insufficient_funds", "timestamp": 1680123457}
{"type": "InventoryReleased", "saga_id": "saga42", "reservation_id": "r1", "timestamp": 1680123458}
```

**编排执行示例**：
```json
// Client starts saga by calling InventoryService:
Request:  {"type": "reserve_inventory", "msg_id": 1, "saga_id": "saga42", "sku": "abc123", "quantity": 1}
Response: {"type": "reserve_inventory_ok", "in_reply_to": 1, "saga_id": "saga42", "reservation_id": "r1"}

// InventoryService publishes event, PaymentService picks it up:
{"type": "InventoryReserved", "saga_id": "saga42", "reservation_id": "r1"}

// PaymentService charges and publishes event:
{"type": "PaymentCharged", "saga_id": "saga42", "payment_id": "p1", "amount": 99.99}

// ShippingService creates shipment and publishes event:
{"type": "ShipmentCreated", "saga_id": "saga42", "shipment_id": "s1"}
```

**编排模式下的故障处理**：
```json
// If payment fails:
{"type": "PaymentFailed", "saga_id": "saga42", "reason": "insufficient_funds"}

// InventoryService subscribes to PaymentFailed and runs compensator:
{"type": "InventoryReleased", "saga_id": "saga42", "reservation_id": "r1"}
```

## 涉及概念

- `choreography`
- `event-driven architecture`
- `service coordination`
- `no central orchestrator`
- `event publishing`

## 实现提示

- 每个服务完成自己的步骤后发布事件
- 下一个服务订阅这些事件并做出响应
- 没有集中式协调者：服务之间仅通过事件通信
- 例如：库存服务发布 "InventoryReserved" 事件，支付服务订阅该事件后执行扣款
- 使用消息代理或事件总线来广播事件

## 测试用例

### 1. 编排式 Saga 成功完成

编排应按顺序完成：库存 → 支付 → 物流事件依次触发。

输入：

```json
{"src":"c0","dest":"event_bus","body":{"type":"init","msg_id":1,"services":["inventory","payment","shipping"]}}
{"src":"c1","dest":"inventory","body":{"type":"reserve_inventory","msg_id":2,"saga_id":"saga42","sku":"abc123","quantity":1}}
```

期望输出：

```text
{"src": "event_bus", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 编排式 Saga 处理支付失败

当支付失败时，应触发 InventoryReleased 事件来补偿库存预留。

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

- [Choreography vs Orchestration](https://www.nginx.com/blog/nginx-microservices-reference-architecture-nginxa-microservices-reference-architecture-part3-choreography-vs-orchestration/)：编排模式与协调模式的对比

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
