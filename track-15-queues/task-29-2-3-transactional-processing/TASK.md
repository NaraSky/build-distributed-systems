# Implement Transactional Message Processing

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-3-transactional-processing>

Track: 15. Queues
Task order: 8
Short title: Transactional Processing
Difficulty: advanced
Subtrack: Exactly-Once Delivery

## Problem

Transactional message processing ensures atomicity between message consumption and database updates, enabling exactly-once semantics through coordinated commits.

**Transactional processing problem**: Message processing and state updates must be atomic. Scenario demonstrates the issue: 1) Consumer receives message, 2) Consumer updates database, 3) Consumer crashes before ACK, 4) Queue re-delivers message, 5) Consumer updates database again causing duplicate. Solution uses transactional processing: Read message, process message (update database), commit offset, all in one atomic transaction. Benefits: No partial updates, no duplicate processing, consistent state, exactly-once semantics.

**Transactional consumer**: TransactionResult interface with success boolean, optional offset, optional error string. TransactionalConsumer class maintains MessageQueue and Database instances. consume method implements transactional processing: Start database transaction, process message within transaction, commit database transaction, ACK message (only after DB commit), return success with offset. On error: Rollback database transaction, don't ACK message (will be re-delivered), return failure with error message. processMessage method (protected, override in subclass) handles actual message processing logic.

**Example payment processing**: PaymentProcessor extends TransactionalConsumer. processMessage method extracts userId, amount, paymentId from message data. Checks if payment already exists for idempotency (SELECT query by payment_id). Returns early if payment exists (prevents duplicates). Inserts payment record with payment_id, user_id, amount, status completed, and timestamp. Updates user balance by adding amount. All database operations within same transaction ensure atomicity.

**Queue and database coordination**: QueueDatabaseCoordinator interface defines readMessage, processMessage, commit, and rollback methods. ExactlyOnceCoordinator class implements coordination between queue and database. processExactlyOnce method: Start database transaction, process message with handler function, commit database transaction, ACK message in queue. On error: Rollback database transaction, don't ACK message, throw error for retry. processBatch method processes multiple messages sequentially using processExactlyOnce for each.

**Transaction isolation levels**: IsolationLevel enum defines READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE. TransactionalConsumerWithIsolation class allows specifying isolation level. consume method starts transaction with configured isolation level, processes message, commits transaction, ACKs message. On error rolls back transaction. Higher isolation levels prevent concurrent modification issues but may reduce concurrency.

**Dead letter queue handling**: TransactionalConsumerWithDLQ extends TransactionalConsumer with retry logic. Maintains maxRetries (default 3), retryCounts map, and dead letter queue reference. consume method checks retry count for message, attempts normal processing via super.consume, resets retry count on success. On failure: Increments retry count, checks if max retries exceeded, sends message to DLQ with error context if max exceeded, ACKs original message to remove from main queue, returns failure. If retries remaining, doesn't ACK (will be retried). sendToDLQ method creates DLQ message with original data plus error information and failed timestamp.

**Example transactional flow**: Create ExactlyOnceCoordinator with queue and database. Process message with handler that updates user balance. Success flow: Processing message logged, database transaction committed, message acknowledged, user balance updated. Failure flow: Processing message logged, error occurs (e.g., insufficient funds), database transaction rolled back, message not acknowledged (will be re-delivered for retry).

**Example transactional scenarios**: Scenario 1 successful transaction: Message received, begin transaction, update database, commit transaction, ACK message, result success. Scenario 2 failed transaction: Message received, begin transaction, update database, error occurs (insufficient funds), rollback transaction, no ACK, result will retry.

**Key benefits**: Atomic operations ensure message processing and state updates succeed or fail together, commit offset only after successful processing prevents duplicates, rollback on failure undoes partial updates, database ACID properties maintain consistency, queue integration coordinates message acknowledgment with transaction commit, dead letter queue handles permanently failed messages.

## Concepts

- transactional processing
- atomic operations
- database transactions
- message acknowledgment
- exactly-once semantics

## Hints

- Atomic operations: Process message and update state in one transaction
- Commit offset: Only ACK after successful processing
- Rollback on failure: Undo processing if commit fails
- Database transactions: Use ACID properties for consistency
- Queue integration: Coordinate queue and database commits

## Test Cases

### 1. Process message transactionally

Should process message and commit transaction.

Input:

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-1","data":{"user_id":"user-123","amount":100}}}}
```

Expected output:

```text
{"type": "processed", "in_reply_to": 1, "message_id": "msg-1", "committed": true, "acked": true}
```

### 2. Rollback on failure

Should rollback transaction on processing failure.

Input:

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-2","data":{"user_id":"user-456","amount":-1000}}}}
```

Expected output:

```text
{"type": "failed", "in_reply_to": 1, "message_id": "msg-2", "rolled_back": true, "acked": false}
```

## Resources

- [Transactional Messaging](https://www.enterpriseintegrationpatterns.com/patterns/messaging/TransactionalClient.html): Transactional client pattern

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
