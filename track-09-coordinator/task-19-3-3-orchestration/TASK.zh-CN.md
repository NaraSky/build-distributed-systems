# 实现 Orchestration-Based Saga

英文标题：Implement Orchestration-Based Saga
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-3-orchestration>

课程：9. 协调器：分布式事务
任务序号：13
短标题：Orchestration Saga
难度：intermediate
子主题：Saga Pattern

## 中文导读

本题要求你完成 `实现 Orchestration-Based Saga`。

重点关注：`orchestration`、`saga orchestrator`、`central coordinator`、`state machine`、`command patterns`。

建议先按提示逐步实现：A saga orchestrator sends commands to services和listens用于replies。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In an orchestration-based saga, a central orchestrator manages the saga lifecycle. It sends commands to services, tracks completion,和initiates compensating transactions on 故障.

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
```JSON
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
    事务: string;
    params: any;
    status: "PENDING" | "COMPLETED" | "FAILED" | "COMPENSATED";
    result?: any;
  }>;
}
```

**Example orchestration execution**:
```JSON
请求:  {"type": "saga_begin", "msg_id": 1, "saga_id": "saga42", "steps": [
    {"事务": "ReserveInventory", "service": "inventory", "params": {"sku": "abc123", "quantity": 1}},
    {"事务": "ChargePayment", "service": "payment", "params": {"user_id": "u42", "amount": 99.99}},
    {"事务": "CreateShipment", "service": "shipping", "params": {"order_id": "o123"}}
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

## 涉及概念

- `orchestration`
- `saga orchestrator`
- `central coordinator`
- `state machine`
- `command patterns`

## 实现提示

- A saga orchestrator sends commands to services和listens用于replies
- The orchestrator maintains the saga state machine (pending, completed, aborted)
- On 故障, orchestrator sends compensating commands in reverse order
- Orchestrator persists state用于recovery after crashes
- Example: orchestrator → ChargePayment → payment service → orchestrator

## 测试用例

### 1. Orchestrator completes saga successfully

Orchestrator should execute all 3 steps sequentially和complete，包含status=COMPLETED.

输入：

```json
{"src":"c0","dest":"orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga42","steps":[{"transaction":"ReserveInventory","service":"inventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","service":"payment","params":{"user_id":"u42","amount":50}},{"transaction":"CreateShipment","service":"shipping","params":{"order_id":"o123"}}]}}
```

期望输出：

```text
{"src": "orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Orchestrator compensates on failure

When payment fails, orchestrator should send ReleaseReservation command和abort，包含status=ABORTED.

输入：

```json
{"src":"c0","dest":"orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga43","steps":[{"transaction":"ReserveInventory","service":"inventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","service":"payment","params":{"user_id":"u999","amount":99999}},{"transaction":"CreateShipment","service":"shipping","params":{"order_id":"o124"}}]}}
```

期望输出：

```text
{"src": "orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Saga Orchestration Pattern](https://www.ibm.com/cloud/architecture/architectures/orchestration-saga-pattern)：IBM documentation on saga orchestration

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
