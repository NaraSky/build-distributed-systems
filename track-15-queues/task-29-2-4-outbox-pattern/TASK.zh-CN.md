# 实现发件箱模式

英文标题：Implement Outbox Pattern
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-4-outbox-pattern>

课程：15. 队列
任务序号：9
短标题：发件箱模式
难度：高级
子主题：精确一次投递

## 中文导读

本题要求你实现发件箱模式（Outbox Pattern），解决"业务数据已更新但消息发送失败"这一经典难题。核心思路是：不直接发消息到队列，而是将消息写入数据库的发件箱表，与业务数据在同一个事务中提交，然后由后台进程异步读取发件箱并发布消息。这样就能保证业务数据和消息的一致性。

## 题目说明

**发件箱模式要解决的问题**：

如何可靠地发布消息？看一个典型的问题场景：
1. 开启数据库事务
2. 更新业务数据（例如创建订单）
3. 提交事务
4. 向消息队列发送消息
5. 第 4 步失败了（队列宕机或网络故障）
6. 消息永远没有发出去
7. 订单创建了，但通知没有发送

发件箱模式的解决方案：
1. 开启数据库事务
2. 更新业务数据（创建订单）
3. 将消息写入发件箱表
4. 提交事务（原子操作，要么全成功要么全失败）
5. 后台进程读取发件箱中的未处理消息
6. 将消息发布到队列
7. 标记消息为已处理

好处是：业务数据和消息创建是原子的，不会丢消息，最终一致，容错性强。

**发件箱表结构**：

```sql
CREATE TABLE outbox (
    id BIGSERIAL PRIMARY KEY,
    aggregate_type VARCHAR(255) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    processed_at TIMESTAMP,
    UNIQUE(aggregate_type, aggregate_id, event_type)
);
CREATE INDEX idx_outbox_created ON outbox(created_at);
```

**发件箱消息发布器**：

```typescript
id: number;
aggregateType: string;
aggregateId: string;
eventType: string;
payload: any;
createdAt: Date;
processed: boolean;
processedAt?: Date;

private database: Database;
private messageQueue: MessageQueue;
private pollingIntervalMs = 1000; // 1 second
private batchSize = 100;

this.database = database;
this.messageQueue = messageQueue;

// Start polling for unprocessed messages
console.log('Starting outbox publisher...');
await this.processBatch();

// Process batch of unprocessed messages
// Get unprocessed messages
const messages = await this.getUnprocessedMessages(this.batchSize);
return;
// Publish each message
await this.publishMessage(message);
console.error('Error processing outbox batch:', error);

// Get unprocessed messages
const result = await this.database.query(
    `SELECT * FROM outbox
     WHERE processed = FALSE
     ORDER BY created_at ASC
     LIMIT $1
     FOR UPDATE SKIP LOCKED`,
    [limit]
);

return result.rows;

// Publish single message
private async publishMessage(message: OutboxMessage): Promise<void> {
    try {
        console.log(`Publishing outbox message ${message.id}`);

        // Publish to message queue
        await this.messageQueue.send({
            type: message.eventType,
            aggregateType: message.aggregateType,
            aggregateId: message.aggregateId,
            payload: message.payload
        });

        // Mark as processed
        await this.markAsProcessed(message.id);

        console.log(`Outbox message ${message.id} published and marked as processed`);

    } catch (error) {
        console.error(`Failed to publish outbox message ${message.id}:`, error);

        // Don't mark as processed (will be retried)
    }
}

// Mark message as processed
private async markAsProcessed(messageId: number): Promise<void> {
    await this.database.query(
        `UPDATE outbox
         SET processed = TRUE,
             processed_at = NOW()
         WHERE id = $1`,
        [messageId]
    );
}

// Cleanup old processed messages
async cleanup(olderThanHours: number = 24): Promise<void> {
    const cutoff = new Date();
    cutoff.setHours(cutoff.getHours() - olderThanHours);

    const result = await this.database.query(
        `DELETE FROM outbox
         WHERE processed = TRUE
         AND processed_at < $1`,
        [cutoff]
    );

    console.log(`Cleaned up ${result.rowCount} old outbox messages`);
}
```

**发件箱消息写入器**：

```typescript
class OutboxWriter {
    private database: Database;

    constructor(database: Database) {
        this.database = database;
    }

    // Write business data and outbox messages atomically
    async writeInTransaction<T>(
        businessData: T,
        events: OutboxEvent[]
    ): Promise<void> {
        await this.database.transaction(async (trx) => {
            // Write business data
            await this.writeBusinessData(businessData, trx);

            // Write outbox messages
            for (const event of events) {
                await this.writeOutboxMessage(event, trx);
            }
        });

        console.log(`Business data and ${events.length} outbox messages written atomically`);
    }

    // Write business data
    private async writeBusinessData<T>( T, trx: any): Promise<void> {
        // Implement business data writing
        console.log('Writing business data:', data);
    }

    // Write outbox message
    private async writeOutboxMessage(event: OutboxEvent, trx: any): Promise<void> {
        await trx.query(
            `INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload)
             VALUES ($1, $2, $3, $4)`,
            [event.aggregateType, event.aggregateId, event.eventType, JSON.stringify(event.payload)]
        );
    }
}

interface OutboxEvent {
    aggregateType: string;
    aggregateId: string;
    eventType: string;
    payload: any;
}
```

**示例：使用发件箱创建订单**：

```typescript
class OrderService {
    private database: Database;
    private outboxWriter: OutboxWriter;

    constructor(database: Database) {
        this.database = database;
        this.outboxWriter = new OutboxWriter(database);
    }

    // Create order with events
    async createOrder(orderData: CreateOrderRequest): Promise<Order> {
        console.log(`Creating order for user ${orderData.userId}`);

        // Business data
        const order = {
            id: generateOrderId(),
            userId: orderData.userId,
            items: orderData.items,
            total: calculateTotal(orderData.items),
            status: 'created',
            createdAt: new Date()
        };

        // Events to publish
        const events: OutboxEvent[] = [
            {
                aggregateType: 'Order',
                aggregateId: order.id,
                eventType: 'OrderCreated',
                payload: {
                    orderId: order.id,
                    userId: order.userId,
                    total: order.total
                }
            },
            {
                aggregateType: 'Order',
                aggregateId: order.id,
                eventType: 'PaymentRequested',
                payload: {
                    orderId: order.id,
                    amount: order.total
                }
            }
        ];

        // Write order and events atomically
        await this.outboxWriter.writeInTransaction(order, events);

        console.log(`Order ${order.id} created with ${events.length} events`);

        return order;
    }
}
```

**幂等的发件箱处理**：

```typescript
class IdempotentOutboxPublisher extends OutboxPublisher {
    private publishedMessageIds: Set<string> = new Set();

    // Override publish to add idempotency
    protected async publishMessage(message: OutboxMessage): Promise<void> {
        // Check if already published
        const messageKey = `${message.aggregateType}:${message.aggregateId}:${message.eventType}`;

        if (this.publishedMessageIds.has(messageKey)) {
            console.log(`Message ${messageKey} already published, skipping`);

            await this.markAsProcessed(message.id);

            return;
        }

        // Publish message
        await super.publishMessage(message);

        // Mark as published
        this.publishedMessageIds.add(messageKey);
    }

    // Cleanup published message IDs
    cleanupPublishedIds(olderThanHours: number = 1): void {
        const cutoff = Date.now() - (olderThanHours * 60 * 60 * 1000);

        // This would need to be implemented based on your tracking mechanism
        console.log(`Cleanup published IDs older than ${olderThanHours} hours`);
    }
}
```

**结合 Kafka 的事务性发件箱**：

```typescript
class KafkaOutboxPublisher {
    private database: Database;
    private kafkaProducer: Producer;
    private topic: string;

    constructor(database: Database, kafkaProducer: Producer, topic: string) {
        this.database = database;
        this.kafkaProducer = kafkaProducer;
        this.topic = topic;
    }

    async processBatch(): Promise<void> {
        const messages = await this.getUnprocessedMessages(100);

        for (const message of messages) {
            try {
                // Send to Kafka
                await this.kafkaProducer.send({
                    topic: this.topic,
                    key: message.aggregateId,
                    value: JSON.stringify({
                        type: message.eventType,
                        aggregateType: message.aggregateType,
                        aggregateId: message.aggregateId,
                        payload: message.payload
                    })
                });

                // Mark as processed
                await this.markAsProcessed(message.id);

                console.log(`Outbox message ${message.id} sent to Kafka`);

            } catch (error) {
                console.error(`Failed to send to Kafka:`, error);

                // Don't mark as processed (will retry)
            }
        }
    }
}
```

**发件箱流程示例**：

```typescript
// Create order with outbox
const orderService = new OrderService(database);

await orderService.createOrder({
    userId: 'user-123',
    items: [
        { productId: 'prod-1', quantity: 2 },
        { productId: 'prod-2', quantity: 1 }
    ]
});

// Output:
// Creating order for user user-123
// Business data and 2 outbox messages written atomically
// Order order-123 created with 2 events

// Background outbox publisher processes events:
// Processing 2 outbox messages
// Publishing outbox message 1
// Published OrderCreated event for order order-123
// Publishing outbox message 2
// Published PaymentRequested event for order order-123
// Outbox message 1 published and marked as processed
// Outbox message 2 published and marked as processed
```

**发件箱场景示例**：

```json
// Scenario 1: Atomic write
{
  "transaction": [
    {"action": "insert_order", "order_id": "order-123"},
    {"action": "insert_outbox", "event_type": "OrderCreated"},
    {"action": "insert_outbox", "event_type": "PaymentRequested"},
    {"action": "commit"}
  ],
  "result": "all_or_nothing"
}

// Scenario 2: Background publishing
{
  "outbox_processing": [
    {"action": "read_unprocessed", "count": 2},
    {"action": "publish_to_queue", "event": "OrderCreated"},
    {"action": "mark_processed", "outbox_id": 1},
    {"action": "publish_to_queue", "event": "PaymentRequested"},
    {"action": "mark_processed", "outbox_id": 2}
  ],
  "result": "events_published"
}
```

## 涉及概念

- `outbox pattern`
- `event publishing`
- `database transactions`
- `message reliability`
- `eventual consistency`
- `publisher reliability`

## 实现提示

- 发件箱表：将消息存储在数据库表中
- 原子写入：在一个事务中同时写入业务数据和发件箱消息
- 独立发布器：后台进程读取发件箱并发布消息
- 幂等发布：记录已发布的消息，避免重复发布
- 清理机制：确认发布后删除已处理的发件箱记录

## 测试用例

### 1. 原子写入发件箱

应当原子地写入业务数据和发件箱事件。

输入：

```json
{"src":"service","dest":"outbox","body":{"type":"write","msg_id":1,"business_data":{"order_id":"order-123"},"events":[{"type":"OrderCreated"},{"type":"PaymentRequested"}]}}
```

期望输出：

```text
{"type": "written", "in_reply_to": 1, "order_id": "order-123", "outbox_events": 2}
```

### 2. 发布发件箱消息

应当将发件箱中的消息发布到队列。

输入：

```json
{"src":"publisher","dest":"queue","body":{"type":"publish","msg_id":1,"outbox_messages":[{"id":1,"event_type":"OrderCreated","payload":{"order_id":"order-123"}}]}}
```

期望输出：

```text
{"type": "published", "in_reply_to": 1, "published_count": 1, "marked_processed": true}
```

## 参考资料

- [Outbox Pattern](https://www.eventstore.com/blog/event-sourcing-with-the-outbox-pattern/)：发件箱模式实现可靠消息发布

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
