# 实现幂等消费者

英文标题：Implement Idempotent Consumers
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-2-idempotent-consumers>

课程：15. 队列
任务序号：7
短标题：幂等消费者
难度：进阶
子主题：精确一次投递

## 中文导读

本题要求你实现幂等消费者（Idempotent Consumer），即使同一条消息被投递多次，也只会产生一次业务效果。这是实现精确一次处理的关键技术之一。通过记录已处理的消息标识并在处理前进行查重，消费者可以安全地应对重复投递。

## 题目说明

**幂等消费者**：

在分布式系统中，消息可能被多次投递，原因包括：
1. 消费者在发送确认之前崩溃
2. 网络故障
3. 队列的重新投递机制
4. 生产者的重试

解决方案是幂等处理——同一条消息处理 N 次的结果与处理一次完全相同。具体做法是：记录已处理的消息标识，遇到重复消息时跳过。

例如，消息内容是"将产品 X 的库存减 1"。如果没有幂等保护，处理两次就会减两次库存。

**幂等消费者的实现**：

```typescript
messageId: string;
processedAt: Date;
result?: any;

private processedMessages: Map<string, ProcessedMessage> = new Map();
private maxStoredMessages = 100000; // Limit memory usage

// Consume message idempotently
const messageId = message.id;
// Check if already processed
// Return cached result
return this.getProcessedResult(messageId);
// Process message
const result = await this.processMessage(message);
// Mark as processed
this.markAsProcessed(messageId, result);
return result;

// Check if message is processed
return this.processedMessages.has(messageId);

// Get processed result
const processed = this.processedMessages.get(messageId);
return processed?.result;

// Mark message as processed
messageId,
processedAt: new Date(),
result
// Cleanup old messages if needed
this.cleanupOldMessages();

// Cleanup old processed messages
const entries = Array.from(this.processedMessages.entries());
// Sort by processed time
// Remove oldest 10%
const toRemove = Math.floor(this.maxStoredMessages * 0.1);
const [messageId] = entries[i];
this.processedMessages.delete(messageId);

// Process message (implement in subclass)
// Default implementation
```

**基于数据库的去重**：

```typescript
private db: Database;

super();
this.db = db;

// Check if message is processed in database
const result = await this.db.query(
    'SELECT 1 FROM processed_messages WHERE message_id = $1',
    [messageId]
);
return result.rows.length > 0;

// Get processed result from database
const result = await this.db.query(
    'SELECT result FROM processed_messages WHERE message_id = $1',
    [messageId]
);
return JSON.parse(result.rows[0].result);
return undefined;

// Mark message as processed in database
await this.db.query(
    `INSERT INTO processed_messages (message_id, processed_at, result)
     VALUES ($1, $2, $3)
     ON CONFLICT (message_id) DO NOTHING`,
    [messageId, new Date(), JSON.stringify(result)]
);

console.log(`Message ${messageId} marked as processed in database`);

// Override consume to use database
async consume(message: Message): Promise<any> {
    const messageId = message.id;

    // Check if already processed
    if (await this.isProcessed(messageId)) {
        console.log(`Message ${messageId} already processed, skipping`);

        return await this.getProcessedResult(messageId);
    }

    console.log(`Processing message ${messageId}`);

    // Process message in transaction
    const result = await this.db.transaction(async (trx) => {
        // Process business logic
        const processedResult = await this.processMessageWithTransaction(message, trx);

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

// Process message with transaction
protected async processMessageWithTransaction(message: Message, trx: any): Promise<any> {
    // Implement business logic
    return { success: true };
}
```

**幂等键**：

```typescript
// Use business keys instead of message IDs
interface IdempotencyKey {
    key: string;
    value: string;
}

class IdempotencyKeyConsumer {
    private processedKeys: Map<string, ProcessedMessage> = new Map();

    // Generate idempotency key from message
    private generateIdempotencyKey(message: Message): string {
        // Use business logic to create unique key
        const parts = [
            message.type,
            message.userId,
            message.resourceId,
            message.action
        ];

        return parts.join(':');
    }

    // Consume message with idempotency key
    async consume(message: Message): Promise<any> {
        const idempotencyKey = this.generateIdempotencyKey(message);

        console.log(`Processing message with idempotency key: ${idempotencyKey}`);

        // Check if key is processed
        if (this.processedKeys.has(idempotencyKey)) {
            console.log(`Idempotency key ${idempotencyKey} already processed`);

            return this.processedKeys.get(idempotencyKey)?.result;
        }

        // Process message
        const result = await this.processMessage(message);

        // Mark key as processed
        this.processedKeys.set(idempotencyKey, {
            messageId: message.id,
            processedAt: new Date(),
            result
        });

        return result;
    }

    private async processMessage(message: Message): Promise<any> {
        // Process message
        return { success: true };
    }
}

// Example: Payment processing
class PaymentConsumer extends IdempotencyKeyConsumer {
    protected generateIdempotencyKey(message: Message): string {
        // Use payment ID as idempotency key
        return `payment:${message.paymentId}`;
    }

    protected async processMessage(message: Message): Promise<any> {
        const { paymentId, amount, userId } = message;

        // Check if payment already processed
        const existingPayment = await this.db.query(
            'SELECT * FROM payments WHERE payment_id = $1',
            [paymentId]
        );

        if (existingPayment.rows.length > 0) {
            console.log(`Payment ${paymentId} already processed`);

            return existingPayment.rows[0];
        }

        // Process payment
        const result = await this.db.query(
            `INSERT INTO payments (payment_id, user_id, amount, status)
             VALUES ($1, $2, $3, 'completed')
             RETURNING *`,
            [paymentId, userId, amount]
        );

        console.log(`Payment ${paymentId} processed successfully`);

        return result.rows[0];
    }
}
```

**幂等操作**：

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

    // Idempotent increment using conditional update
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
            console.log(`Increment for message ${messageId} already applied`);

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

**幂等消费者的流程示例**：

```typescript
// Create idempotent consumer
const consumer = new DatabaseIdempotentConsumer(database);

// Process messages
const messages = [
    { id: 'msg-1', type: 'payment', paymentId: 'pay-123', amount: 100 },
    { id: 'msg-2', type: 'payment', paymentId: 'pay-124', amount: 200 },
    { id: 'msg-1', type: 'payment', paymentId: 'pay-123', amount: 100 }  // Duplicate!
];

for (const message of messages) {
    await consumer.consume(message);
}

// Output:
// Processing message msg-1
// Payment pay-123 processed successfully
// Processing message msg-2
// Payment pay-124 processed successfully
// Message msg-1 already processed, skipping
```

**幂等场景示例**：

```json
// Scenario 1: Deduplicate by message ID
{
  "message": {"id": "msg-1", "action": "decrement_inventory"},
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
  "message": {"id": "msg-2", "payment_id": "pay-123"},
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

- 唯一消息标识：每条消息都有唯一的标识符
- 记录已处理消息：将消息标识存储在数据库或缓存中
- 处理前检查：如果消息已处理过就跳过
- 幂等键：可以使用业务键替代消息标识来判断是否重复
- 清理策略：定期清除过期的已处理记录，防止内存泄漏

## 测试用例

### 1. 跳过已处理的消息

应当跳过已经处理过的消息。

输入：

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-1"},"processed":["msg-1"]}}
```

期望输出：

```text
{"type": "skipped", "in_reply_to": 1, "message_id": "msg-1", "reason": "already_processed"}
```

### 2. 处理新消息

应当成功处理新消息。

输入：

```json
{"src":"consumer","dest":"processor","body":{"type":"consume","msg_id":1,"message":{"id":"msg-2"},"processed":[]}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "message_id": "msg-2", "result": {"success": true}}
```

## 参考资料

- [Idempotent Consumers](https://www.cloudkarafka.com/blog/part-1-idempotent-consumers-in-kafka/)：如何构建幂等消费者

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
