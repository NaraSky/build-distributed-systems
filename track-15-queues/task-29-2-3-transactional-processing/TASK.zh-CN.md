# 实现 Transactional 消息 Processing

英文标题：Implement Transactional Message Processing
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-3-transactional-processing>

课程：15. 队列
任务序号：8
短标题：Transactional Processing
难度：advanced
子主题：Exactly-Once Delivery

## 中文导读

本题要求你完成 `实现 Transactional 消息 Processing`。

重点关注：`transactional processing`、`atomic operations`、`database transactions`、`message acknowledgment`、`exactly-once semantics`。

建议先按提示逐步实现：Atomic operations: Process 消息和update state in one 事务。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Transactional 消息 processing ensures atomicity between 消息 consumption和database updates, enabling exactly-once semantics through coordinated commits.

**Transactional processing problem**: 消息 processing和state updates must be atomic. Scenario demonstrates the issue: 1) Consumer receives 消息, 2) Consumer updates database, 3) Consumer crashes before ACK, 4) 队列 re-delivers 消息, 5) Consumer updates database again causing duplicate. Solution uses transactional processing: Read 消息, process 消息 (update database), commit offset, all in one atomic 事务. Benefits: No partial updates, no duplicate processing, consistent state, exactly-once semantics.

**Transactional consumer**: TransactionResult interface，包含success boolean, optional offset, optional error string. TransactionalConsumer class maintains MessageQueue和Database instances. consume method implements transactional processing: Start database 事务, process 消息 within 事务, commit database 事务, ACK 消息 (only after DB commit), return success，包含offset. On error: Rollback database 事务, don't ACK 消息 (will be re-delivered), return 故障，包含error 消息. processMessage method (protected, override in subclass) handles actual 消息 processing logic.

**Example payment processing**: PaymentProcessor extends TransactionalConsumer. processMessage method extracts userId, amount, paymentId from 消息 data. Checks if payment already exists用于idempotency (SELECT query by payment_id). Returns early if payment exists (prevents duplicates). Inserts payment record，包含payment_id, user_id, amount, status completed,和timestamp. Updates user balance by adding amount. All database operations within same 事务 ensure atomicity.

**队列和database coordination**: QueueDatabaseCoordinator interface defines readMessage, processMessage, commit,和rollback methods. ExactlyOnceCoordinator class implements coordination between 队列和database. processExactlyOnce method: Start database 事务, process 消息，包含handler function, commit database 事务, ACK 消息 in 队列. On error: Rollback database 事务, don't ACK 消息, throw error用于重试. processBatch method processes multiple 消息 sequentially使用processExactlyOnce用于each.

**事务 isolation levels**: IsolationLevel enum defines READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE. TransactionalConsumerWithIsolation class allows specifying isolation level. consume method starts 事务，包含configured isolation level, processes 消息, commits 事务, ACKs 消息. On error rolls back 事务. Higher isolation levels prevent concurrent modification issues but may reduce concurrency.

**Dead letter 队列 handling**: TransactionalConsumerWithDLQ extends TransactionalConsumer，包含重试 logic. Maintains maxRetries (default 3), retryCounts map,和dead letter 队列 reference. consume method checks 重试 count用于消息, attempts normal processing via super.consume, resets 重试 count on success. On 故障: Increments 重试 count, checks if max retries exceeded, sends 消息 to DLQ，包含error context if max exceeded, ACKs original 消息 to remove from main 队列, returns 故障. If retries remaining, doesn't ACK (will be retried). sendToDLQ method creates DLQ 消息，包含original data plus error information和failed timestamp.

**Example transactional flow**: Create ExactlyOnceCoordinator，包含队列和database. Process 消息，包含handler that updates user balance. Success flow: Processing 消息 logged, database 事务 committed, 消息 acknowledged, user balance updated. 故障 flow: Processing 消息 logged, error occurs (e.g., insufficient funds), database 事务 rolled back, 消息 not acknowledged (will be re-delivered用于重试).

**Example transactional scenarios**: Scenario 1 successful 事务: 消息 received, begin 事务, update database, commit 事务, ACK 消息, result success. Scenario 2 failed 事务: 消息 received, begin 事务, update database, error occurs (insufficient funds), rollback 事务, no ACK, result will 重试.

**Key benefits**: Atomic operations ensure 消息 processing和state updates succeed or fail together, commit offset only after successful processing prevents duplicates, rollback on 故障 undoes partial updates, database ACID properties maintain consistency, 队列 integration coordinates 消息 acknowledgment，包含事务 commit, dead letter 队列 handles permanently failed 消息.

## 涉及概念

- `transactional processing`
- `atomic operations`
- `database transactions`
- `message acknowledgment`
- `exactly-once semantics`

## 实现提示

- Atomic operations: Process 消息和update state in one 事务
- Commit offset: Only ACK after successful processing
- Rollback on 故障: Undo processing if commit fails
- Database transactions: Use ACID properties用于consistency
- 队列 integration: Coordinate 队列和database commits

## 测试用例

### 1. Process 消息 transactionally

Should process 消息和commit 事务.

输入：

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-1","data":{"user_id":"user-123","amount":100}}}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "message_id": "msg-1", "committed": true, "acked": true}
```

### 2. Rollback on failure

Should rollback 事务 on processing 故障.

输入：

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-2","data":{"user_id":"user-456","amount":-1000}}}}
```

期望输出：

```text
{"type": "failed", "in_reply_to": 1, "message_id": "msg-2", "rolled_back": true, "acked": false}
```

## 参考资料

- [Transactional Messaging](https://www.enterpriseintegrationpatterns.com/patterns/messaging/TransactionalClient.html)：Transactional 客户端 pattern

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
