# 实现带补偿事务的 Saga 模式

英文标题：Implement Saga Pattern with Compensating Transactions
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-3-1-saga-fundamentals>

课程：9. 协调器：分布式事务
任务序号：11
短标题：Saga Fundamentals
难度：进阶
子主题：Saga Pattern

## 中文导读

本题要求你实现 Saga 模式的基本机制：将长事务拆分为一系列本地事务，每个本地事务都有对应的补偿操作。当某一步失败时，按相反顺序执行前面步骤的补偿操作来回滚。与两阶段提交不同，Saga 中每一步都立即提交，不需要全局锁。这是微服务架构中处理分布式事务的核心模式。

## 题目说明

Saga 模式通过将长事务拆分为一连串本地事务来管理分布式事务，每个本地事务都有配套的补偿操作用于回滚。与两阶段提交不同的是，每一步完成后就立即提交，但可以通过补偿事务来"撤销"。

**Saga 的结构**：
```
事务序列：T1, T2, ..., Tn
补偿序列：C1, C2, ..., Cn

正向执行：
  T1 → T2 → T3 → ... → Tn（正向路径）

如果 Ti 失败：
  C(i-1) → C(i-2) → ... → C1（反向路径）
```

**电商 Saga 示例**：
```
T1: ReserveInventory（预留库存，sku="abc123", quantity=1）
    C1: ReleaseReservation（释放库存，sku="abc123", quantity=1）

T2: ChargePayment（扣款，user_id="u42", amount=99.99）
    C2: RefundPayment（退款，user_id="u42", amount=99.99）

T3: CreateShipment（创建物流，order_id="o123", address="..."）
    C3: CancelShipment（取消物流，order_id="o123"）
```

**正向执行（正常路径）**：
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

**回滚执行（失败路径）**：
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

## 涉及概念

- `saga pattern`
- `compensating transactions`
- `local transactions`
- `rollback`
- `long-running transactions`

## 实现提示

- 一个 Saga 是一系列本地事务 T1、T2、...、Tn
- 每个事务 Ti 都有对应的补偿事务 Ci
- 如果 Ti 失败，按相反顺序执行 C(i-1)、...、C1 来回滚
- 每个 Ti 独立提交（不像两阶段提交那样锁住所有资源）
- 例如：预留库存（T1） → 扣款（T2） → 创建物流（T3）

## 测试用例

### 1. 成功执行 Saga

saga_begin_ok 应返回 saga_id，Saga 应成功完成所有三个步骤。

输入：

```json
{"src":"c0","dest":"saga_orchestrator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"saga_orchestrator","body":{"type":"saga_begin","msg_id":2,"saga_id":"saga42","steps":[{"transaction":"ReserveInventory","params":{"sku":"abc123","quantity":1}},{"transaction":"ChargePayment","params":{"user_id":"u42","amount":50}},{"transaction":"CreateShipment","params":{"order_id":"o123"}}]}}
```

期望输出：

```text
{"src": "saga_orchestrator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 支付失败时回滚 Saga

当扣款失败时，应执行补偿操作释放库存，Saga 进入已中止状态。

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

- [Saga Pattern](https://microservices.io/patterns/data/saga.html)：microservices.io 上的 Saga 模式文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
