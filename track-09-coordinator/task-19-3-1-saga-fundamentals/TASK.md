# Implement Saga Pattern with Compensating Transactions

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-1-saga-fundamentals>

Track: 9. The Coordinator
Task order: 11
Short title: Saga Fundamentals
Difficulty: intermediate
Subtrack: Saga Pattern

## Problem

The Saga pattern manages long-running transactions by breaking them into a sequence of local transactions with compensating actions for rollback. Unlike 2PC, each step commits immediately, but can be undone by its compensating transaction.

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
```json
Request:  {"type": "saga_begin", "msg_id": 1, "saga_id": "saga42", "steps": [
    {"transaction": "ReserveInventory", "params": {"sku": "abc123", "quantity": 1}},
    {"transaction": "ChargePayment", "params": {"user_id": "u42", "amount": 99.99}},
    {"transaction": "CreateShipment", "params": {"order_id": "o123"}}
]}

Response: {"type": "saga_begin_ok", "in_reply_to": 1, "saga_id": "saga42", "status": "pending"}

// Step 1 completes:
{"type": "step_complete", "saga_id": "saga42", "step": 1, "transaction": "ReserveInventory", "result": "reservation_id=r1"}

// Step 2 completes:
{"type": "step_complete", "saga_id": "saga42", "step": 2, "transaction": "ChargePayment", "result": "payment_id=p1"}

// Step 3 completes:
{"type": "step_complete", "saga_id": "saga42", "step": 3, "transaction": "CreateShipment", "result": "shipment_id=s1"}

// Saga complete:
{"type": "saga_complete", "saga_id": "saga42", "status": "completed"}
```

**Rollback execution (failure path)**:
```json
// Step 1 completes:
{"type": "step_complete", "saga_id": "saga42", "step": 1, "transaction": "ReserveInventory"}

// Step 2 fails:
{"type": "step_failed", "saga_id": "saga42", "step": 2, "transaction": "ChargePayment", "error": "insufficient_funds"}

// Compensating transactions run:
{"type": "compensate", "saga_id": "saga42", "step": 1, "compensator": "ReleaseReservation", "params": {"reservation_id": "r1"}}

// Saga aborted:
{"type": "saga_aborted", "saga_id": "saga42", "status": "aborted", "reason": "Step 2 failed: insufficient_funds"}
```

## Concepts

- saga pattern
- compensating transactions
- local transactions
- rollback
- long-running transactions

## Hints

- A saga is a sequence of local transactions T1, T2, ..., Tn
- Each transaction Ti has a compensating transaction Ci
- If Ti fails, run C(i-1), ..., C1 to rollback
- Each Ti commits locally (no 2PC lock-in)
- Example: ReserveInventory (T1) → ChargePayment (T2) → CreateShipment (T3)

## Test Cases

### 1. Successful saga execution

saga_begin_ok should return saga_id and the saga should complete all 3 steps successfully.

Input:

```json
{"src":"c0","dest":"saga_orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"saga_orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga42","steps":[{"transaction":"ReserveInventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","params":{"user_id":"u42","amount":50}},{"transaction":"CreateShipment","params":{"order_id":"o123"}}]}}
```

Expected output:

```text
{"src": "saga_orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Saga rollback on payment failure

When ChargePayment fails, the compensator ReleaseReservation should run and saga should be aborted.

Input:

```json
{"src":"c0","dest":"saga_orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"saga_orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga43","steps":[{"transaction":"ReserveInventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","params":{"user_id":"u999","amount":99999}},{"transaction":"CreateShipment","params":{"order_id":"o124"}}]}}
```

Expected output:

```text
{"src": "saga_orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Saga Pattern](https://microservices.io/patterns/data/saga.html): Saga pattern documentation from microservices.io

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
