# Implement Choreography-Based Saga

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-2-choreography>

Track: 9. The Coordinator
Task order: 12
Short title: Choreography Saga
Difficulty: advanced
Subtrack: Saga Pattern

## Problem

In a choreography-based saga, there is no central coordinator. Each service listens for events and triggers the next step by publishing its own events. Coordination happens through events, not a orchestrator.

**Choreography flow**:
```
Service A (Inventory)
  → Completes T1
  → Publishes "InventoryReserved" event
  → (if failure) Publishes "InventoryReservationFailed"

Service B (Payment)
  → Subscribes to "InventoryReserved"
  → On event, executes T2 (ChargePayment)
  → Publishes "PaymentCharged" event
  → (if failure) Publishes "PaymentFailed" event

Service C (Shipping)
  → Subscribes to "PaymentCharged"
  → On event, executes T3 (CreateShipment)
  → Publishes "ShipmentCreated" event
  → (if failure) Publishes "ShipmentFailed" event
```

**Event structure**:
```json
// Forward path events:
{"type": "InventoryReserved", "saga_id": "saga42", "reservation_id": "r1", "timestamp": 1680123456}
{"type": "PaymentCharged", "saga_id": "saga42", "payment_id": "p1", "amount": 99.99, "timestamp": 1680123457}
{"type": "ShipmentCreated", "saga_id": "saga42", "shipment_id": "s1", "timestamp": 1680123458}

// Compensating events:
{"type": "PaymentFailed", "saga_id": "saga42", "reason": "insufficient_funds", "timestamp": 1680123457}
{"type": "InventoryReleased", "saga_id": "saga42", "reservation_id": "r1", "timestamp": 1680123458}
```

**Example choreography execution**:
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

**Handling failures in choreography**:
```json
// If payment fails:
{"type": "PaymentFailed", "saga_id": "saga42", "reason": "insufficient_funds"}

// InventoryService subscribes to PaymentFailed and runs compensator:
{"type": "InventoryReleased", "saga_id": "saga42", "reservation_id": "r1"}
```

## Concepts

- choreography
- event-driven architecture
- service coordination
- no central orchestrator
- event publishing

## Hints

- Each service publishes events when it completes its step
- The next service subscribes to those events and reacts
- No central coordinator: services communicate via events only
- Example: InventoryService publishes "InventoryReserved", PaymentService subscribes and charges
- Use a message broker or event bus to broadcast events

## Test Cases

### 1. Choreography completes successfully

Choreography should complete: inventory → payment → shipping events should fire in sequence.

Input:

```json
{"src":"c0","dest":"event_bus","body":{"type":"init","msg_id":1,"services":["inventory","payment","shipping"]}}
{"src":"c1","dest":"inventory","body":{"type":"reserve_inventory","msg_id":2,"saga_id":"saga42","sku":"abc123","quantity":1}}
```

Expected output:

```text
{"src": "event_bus", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Choreography handles payment failure

When payment fails, InventoryReleased event should fire to compensate the reservation.

Input:

```json
{"src":"c0","dest":"event_bus","body":{"type":"init","msg_id":1,"services":["inventory","payment","shipping"]}}
{"src":"c1","dest":"inventory","body":{"type":"reserve_inventory","msg_id":2,"saga_id":"saga43","sku":"abc123","quantity":1,"fail_payment":true}}
```

Expected output:

```text
{"src": "event_bus", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Choreography vs Orchestration](https://www.nginx.com/blog/nginx-microservices-reference-architecture-nginxa-microservices-reference-architecture-part3-choreography-vs-orchestration/): Comparison of choreography and orchestration patterns

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
