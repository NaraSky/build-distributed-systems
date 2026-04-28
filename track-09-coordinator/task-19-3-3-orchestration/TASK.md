# Implement Orchestration-Based Saga

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-3-orchestration>

Track: 9. The Coordinator
Task order: 13
Short title: Orchestration Saga
Difficulty: intermediate
Subtrack: Saga Pattern

## Problem

In an orchestration-based saga, a central orchestrator manages the saga lifecycle. It sends commands to services, tracks completion, and initiates compensating transactions on failure.

**Orchestrator state machine**:
```
States:
  PENDING → Step 1 executing
  Step 1 complete → Step 2 executing
  Step 2 complete → Step 3 executing
  ...
  All steps complete → COMPLETED
  Any step fails → COMPENSATING → ABORTED
```

**Command/reply pattern**:
```json
// Orchestrator sends command:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}

// Service replies:
{"type": "ChargePayment_ok", "saga_id": "saga42", "step": 2, "result": {"payment_id": "p1"}}

// Or fails:
{"type": "ChargePayment_failed", "saga_id": "saga42", "step": 2, "error": "insufficient_funds"}
```

**Orchestrator state structure**:
```typescript
interface SagaState {
  saga_id: string;
  status: "PENDING" | "COMPLETED" | "ABORTED" | "COMPENSATING";
  current_step: number;
  completed_steps: number[];
  compensating_steps: number[];
  steps: Array<{
    transaction: string;
    params: any;
    status: "PENDING" | "COMPLETED" | "FAILED" | "COMPENSATED";
    result?: any;
  }>;
}
```

**Example orchestration execution**:
```json
Request:  {"type": "saga_begin", "msg_id": 1, "saga_id": "saga42", "steps": [
    {"transaction": "ReserveInventory", "service": "inventory", "params": {"sku": "abc123", "quantity": 1}},
    {"transaction": "ChargePayment", "service": "payment", "params": {"user_id": "u42", "amount": 99.99}},
    {"transaction": "CreateShipment", "service": "shipping", "params": {"order_id": "o123"}}
]}

// Orchestrator sends command to inventory:
{"type": "ReserveInventory", "saga_id": "saga42", "step": 1, "params": {"sku": "abc123", "quantity": 1}}

// Inventory replies:
{"type": "ReserveInventory_ok", "saga_id": "saga42", "step": 1, "result": {"reservation_id": "r1"}}

// Orchestrator sends command to payment:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}

// Payment fails:
{"type": "ChargePayment_failed", "saga_id": "saga42", "step": 2, "error": "insufficient_funds"}

// Orchestrator initiates compensation:
{"type": "ReleaseReservation", "saga_id": "saga42", "step": 1, "compensating": true}

// Inventory compensates:
{"type": "ReleaseReservation_ok", "saga_id": "saga42", "step": 1}

// Saga aborted:
{"type": "saga_aborted", "saga_id": "saga42", "status": "ABORTED", "reason": "Step 2 failed: insufficient_funds"}
```

## Concepts

- orchestration
- saga orchestrator
- central coordinator
- state machine
- command patterns

## Hints

- A saga orchestrator sends commands to services and listens for replies
- The orchestrator maintains the saga state machine (pending, completed, aborted)
- On failure, orchestrator sends compensating commands in reverse order
- Orchestrator persists state for recovery after crashes
- Example: orchestrator → ChargePayment → payment service → orchestrator

## Test Cases

### 1. Orchestrator completes saga successfully

Orchestrator should execute all 3 steps sequentially and complete with status=COMPLETED.

Input:

```json
{"src":"c0","dest":"orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga42","steps":[{"transaction":"ReserveInventory","service":"inventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","service":"payment","params":{"user_id":"u42","amount":50}},{"transaction":"CreateShipment","service":"shipping","params":{"order_id":"o123"}}]}}
```

Expected output:

```text
{"src": "orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Orchestrator compensates on failure

When payment fails, orchestrator should send ReleaseReservation command and abort with status=ABORTED.

Input:

```json
{"src":"c0","dest":"orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga43","steps":[{"transaction":"ReserveInventory","service":"inventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","service":"payment","params":{"user_id":"u999","amount":99999}},{"transaction":"CreateShipment","service":"shipping","params":{"order_id":"o124"}}]}}
```

Expected output:

```text
{"src": "orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Saga Orchestration Pattern](https://www.ibm.com/cloud/architecture/architectures/orchestration-saga-pattern): IBM documentation on saga orchestration

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
