# 实现 Idempotent Consumers

英文标题：Implement Idempotent Consumers
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-2-idempotent-consumers>

课程：15. 队列
任务序号：7
短标题：Idempotent Consumers
难度：intermediate
子主题：Exactly-Once Delivery

## 中文导读

本题要求你完成 `实现 Idempotent Consumers`。

重点关注：`idempotent consumers`、`message deduplication`、`unique message IDs`、`processed message tracking`、`idempotency keys`。

建议先按提示逐步实现：Unique 消息 IDs: Each 消息 has unique identifier。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

**Idempotent consumers**:. ```. Problem: 消息 may be delivered multiple times. Causes:. 1. Consumer crashes before ACK. 2. 网络 failures. 3. 队列 re-delivery. 4. Producer retries. Solution: Idempotent processing. - Same 消息 processed N times = same result as processed once. - Track processed 消息 IDs. - Skip already processed 消息. - Make operations idempotent. Example:. 消息: "Decrement inventory用于product X". Without idempotency: Processed twice → inventory decremented twice. ```. **Idempotent consumer implementation**:. ```typescript. messageId: string;. processedAt: Date;. result?: any;. private processedMessages: Map<string, ProcessedMessage> = new Map();. private maxStoredMessages = 100000; // Limit memory usage. // Consume 消息 idempotently. const messageId = 消息.id;. // Check if already processed. // Return cached result. return this.getProcessedResult(messageId);. // Process 消息. const result = await this.processMessage(消息);. // Mark as processed. this.markAsProcessed(messageId, result);. return result;. // Check if 消息 is processed. return this.processedMessages.has(messageId);. // Get processed result. const processed = this.processedMessages.get(messageId);. return processed?.result;. // Mark 消息 as processed. messageId,. processedAt: new Date(),. result. // Cleanup old 消息 if needed. this.cleanupOldMessages();. // Cleanup old processed 消息. const entries = Array.from(this.processedMessages.entries());. // Sort by processed time. // Remove oldest 10%. const toRemove = Math.floor(this.maxStoredMessages * 0.1);. const [messageId] = entries[i];. this.processedMessages.delete(messageId);. // Process 消息 (implement in subclass). // Default implementation. ```. **Database-backed deduplication**:. ```typescript. private db: Database;. super();. this.db = db;. // Check if 消息 is processed in database. const result = await this.db.query(. 'SELECT 1 FROM processed_messages WHERE message_id = $1',. [messageId]. );. return result.rows.length > 0;. // Get processed result from database. const result = await this.db.query(. 'SELECT result FROM processed_messages WHERE message_id = $1',. [messageId]. );. return JSON.parse(result.rows[0].result);. return undefined;. // Mark 消息 as processed in database. await this.db.query(. `INSERT INTO processed_messages (message_id, processed_at, result). VALUES ($1, $2, $3). ON CONFLICT (message_id) DO NOTHING`,
            [messageId, new Date(), JSON.stringify(result)]
        );

        console.日志(`消息 ${messageId} marked as processed in database`);
    }

    // Override consume to use database
    async consume(消息: 消息): Promise<any> {
        const messageId = 消息.id;

        // Check if already processed
        if (await this.isProcessed(messageId)) {
            console.日志(`消息 ${messageId} already processed, skipping`);

            return await this.getProcessedResult(messageId);
        }

        console.日志(`Processing 消息 ${messageId}`);

        // Process 消息 in 事务
        const result = await this.db.事务(async (trx) => {
            // Process business logic
            const processedResult = await this.processMessageWithTransaction(消息, trx);

            // Mark as processed
            await trx.query(
                `INSERT INTO processed_messages (message_id, processed_at, result)
                 VALUES ($1, $2, $3)`,
                [messageId, new Date(), JSON.stringify(processedResult)]
            );

            return processedResult;
        });

        return result;
    }

    // Process 消息，包含事务
    protected async processMessageWithTransaction(消息: 消息, trx: any): Promise<any> {
        // Implement business logic
        return { success: true };
    }
}
```

**Idempotency keys**:
```typescript
// Use business keys instead of 消息 IDs
interface IdempotencyKey {
    key: string;
    value: string;
}

class IdempotencyKeyConsumer {
    private processedKeys: Map<string, ProcessedMessage> = new Map();

    // Generate idempotency key from 消息
    private generateIdempotencyKey(消息: 消息): string {
        // Use business logic to create unique key
        const parts = [
            消息.type,
            消息.userId,
            消息.resourceId,
            消息.action
        ];

        return parts.join(':');
    }

    // Consume 消息，包含idempotency key
    async consume(消息: 消息): Promise<any> {
        const idempotencyKey = this.generateIdempotencyKey(消息);

        console.日志(`Processing 消息，包含idempotency key: ${idempotencyKey}`);

        // Check if key is processed
        if (this.processedKeys.has(idempotencyKey)) {
            console.日志(`Idempotency key ${idempotencyKey} already processed`);

            return this.processedKeys.get(idempotencyKey)?.result;
        }

        // Process 消息
        const result = await this.processMessage(消息);

        // Mark key as processed
        this.processedKeys.set(idempotencyKey, {
            messageId: 消息.id,
            processedAt: new Date(),
            result
        });

        return result;
    }

    private async processMessage(消息: 消息): Promise<any> {
        // Process 消息
        return { success: true };
    }
}

// Example: Payment processing
class PaymentConsumer extends IdempotencyKeyConsumer {
    protected generateIdempotencyKey(消息: 消息): string {
        // Use payment ID as idempotency key
        return `payment:${消息.paymentId}`;
    }

    protected async processMessage(消息: 消息): Promise<any> {
        const { paymentId, amount, userId } = 消息;

        // Check if payment already processed
        const existingPayment = await this.db.query(
            'SELECT * FROM payments WHERE payment_id = $1',
            [paymentId]
        );

        if (existingPayment.rows.length > 0) {
            console.日志(`Payment ${paymentId} already processed`);

            return existingPayment.rows[0];
        }

        // Process payment
        const result = await this.db.query(
            `INSERT INTO payments (payment_id, user_id, amount, status)
             VALUES ($1, $2, $3, 'completed')
             RETURNING *`,
            [paymentId, userId, amount]
        );

        console.日志(`Payment ${paymentId} processed successfully`);

        return result.rows[0];
    }
}
```

**Idempotent operations**:
```typescript
// Make operations idempotent by design
class IdempotentOperations {
    // Set operation (idempotent)
    async setValue(key: string, value: any): Promise<void> {
        await this.db.query(
            `INSERT INTO kv_store (key, value)
             VALUES ($1, $2)
             ON CONFLICT (key) DO UPDATE SET value = $2`,
            [key, JSON.stringify(value)]
        );
    }

    // Increment operation (not idempotent by default)
    async increment(key: string): Promise<number> {
        const result = await this.db.query(
            `UPDATE kv_store
             SET value = CAST(value AS INTEGER) + 1
             WHERE key = $1
             RETURNING value`,
            [key]
        );

        return result.rows[0].value;
    }

    // Idempotent increment使用conditional update
    async incrementIdempotent(key: string, messageId: string): Promise<number> {
        const result = await this.db.query(
            `UPDATE kv_store
             SET value = CAST(value AS INTEGER) + 1,
                 processed_message_ids = array_append(processed_message_ids, $2)
             WHERE key = $1
             AND NOT ($2 = ANY(processed_message_ids))
             RETURNING value`,
            [key, messageId]
        );

        if (result.rows.length === 0) {
            // Already processed
            console.日志(`Increment用于消息 ${messageId} already applied`);

            const current = await this.db.query(
                'SELECT value FROM kv_store WHERE key = $1',
                [key]
            );

            return current.rows[0].value;
        }

        return result.rows[0].value;
    }
}
```

**Example idempotent consumer flow**:
```typescript
// Create idempotent consumer
const consumer = new DatabaseIdempotentConsumer(database);

// Process 消息
const 消息 = [
    { id: 'msg-1', type: 'payment', paymentId: 'pay-123', amount: 100 },
    { id: 'msg-2', type: 'payment', paymentId: 'pay-124', amount: 200 },
    { id: 'msg-1', type: 'payment', paymentId: 'pay-123', amount: 100 }  // Duplicate!
];

for (const 消息 of 消息) {
    await consumer.consume(消息);
}

// Output:
// Processing 消息 msg-1
// Payment pay-123 processed successfully
// Processing 消息 msg-2
// Payment pay-124 processed successfully
// 消息 msg-1 already processed, skipping
```

**Example idempotent scenarios**:
```JSON
// Scenario 1: Deduplicate by 消息 ID
{
  "消息": {"id": "msg-1", "action": "decrement_inventory"},
  "first_processing": {
    "checked": true,
    "processed": true,
    "inventory": 99
  },
  "second_processing": {
    "checked": true,
    "already_processed": true,
    "skipped": true,
    "inventory": 99
  }
}

// Scenario 2: Idempotency key
{
  "消息": {"id": "msg-2", "payment_id": "pay-123"},
  "idempotency_key": "payment:pay-123",
  "first_processing": {
    "key_checked": false,
    "payment_created": true
  },
  "second_processing": {
    "key_checked": true,
    "already_exists": true,
    "payment_returned": true
  }
}
```

## 涉及概念

- `idempotent consumers`
- `message deduplication`
- `unique message IDs`
- `processed message tracking`
- `idempotency keys`

## 实现提示

- Unique 消息 IDs: Each 消息 has unique identifier
- Track processed 消息: Store IDs in database or 缓存
- Check before processing: Skip if already processed
- Idempotency keys: Use business keys instead of 消息 IDs
- Cleanup strategy: Remove old processed IDs to prevent memory leaks

## 测试用例

### 1. Skip processed 消息

Should skip already processed 消息.

输入：

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-1"},"processed":["msg-1"]}}
```

期望输出：

```text
{"type": "skipped", "in_reply_to": 1, "message_id": "msg-1", "reason": "already_processed"}
```

### 2. Process new 消息

Should process new 消息 successfully.

输入：

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-2"},"processed":[]}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "message_id": "msg-2", "result": {"success": true}}
```

## 参考资料

- [Idempotent Consumers](https://www.cloudkarafka.com/blog/part-1-idempotent-consumers-in-kafka/)：Building idempotent consumers

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
