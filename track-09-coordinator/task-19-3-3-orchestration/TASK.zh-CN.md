# 实现基于协调器的 Saga

英文标题：Implement Orchestration-Based Saga
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-3-orchestration>

课程：9. 协调器：分布式事务
任务序号：13
短标题：Orchestration Saga
难度：进阶
子主题：Saga Pattern

## 中文导读

本题要求你实现基于协调器（Orchestration）的 Saga。在这种模式下，有一个集中式的协调器来管理整个 Saga 的生命周期：它向各服务发送命令、跟踪执行进度，并在失败时发起补偿事务。相比编排模式，协调模式的流程更清晰、更容易调试，适合复杂的业务场景。

## 题目说明

在基于协调器的 Saga 中，一个集中式的协调器负责管理 Saga 的整个生命周期。它向各服务发送命令，跟踪步骤的完成情况，并在某一步失败时发起补偿事务。

**协调器状态机**：
```
状态流转：
  PENDING → 第 1 步执行中
  第 1 步完成 → 第 2 步执行中
  第 2 步完成 → 第 3 步执行中
  ...
  所有步骤完成 → COMPLETED
  任一步骤失败 → COMPENSATING → ABORTED
```

**命令/回复模式**：
```json
// Orchestrator sends command:
{"type": "ChargePayment", "saga_id": "saga42", "step": 2, "params": {"user_id": "u42", "amount": 99.99}}

// Service replies:
{"type": "ChargePayment_ok", "saga_id": "saga42", "step": 2, "result": {"payment_id": "p1"}}

// Or fails:
{"type": "ChargePayment_failed", "saga_id": "saga42", "step": 2, "error": "insufficient_funds"}
```

**协调器的状态结构**：
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

**协调模式执行示例**：
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

## 涉及概念

- `orchestration`
- `saga orchestrator`
- `central coordinator`
- `state machine`
- `command patterns`

## 实现提示

- Saga 协调器向各服务发送命令并监听回复
- 协调器维护 Saga 的状态机（待处理、已完成、已中止）
- 失败时，协调器按相反顺序发送补偿命令
- 协调器需要持久化状态，以便崩溃后恢复
- 例如：协调器 → 扣款命令 → 支付服务 → 协调器

## 测试用例

### 1. 协调器成功完成 Saga

协调器应按顺序执行所有三个步骤，最终状态为 COMPLETED。

输入：

```json
{"src":"c0","dest":"orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga42","steps":[{"transaction":"ReserveInventory","service":"inventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","service":"payment","params":{"user_id":"u42","amount":50}},{"transaction":"CreateShipment","service":"shipping","params":{"order_id":"o123"}}]}}
```

期望输出：

```text
{"src": "orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 协调器在失败时执行补偿

当支付失败时，协调器应发送释放库存的补偿命令，最终状态为 ABORTED。

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

- [Saga Orchestration Pattern](https://www.ibm.com/cloud/architecture/architectures/orchestration-saga-pattern)：IBM 的 Saga 协调模式文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
