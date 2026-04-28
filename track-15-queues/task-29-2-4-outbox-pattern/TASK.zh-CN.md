# 实现 Outbox Pattern

英文标题：Implement Outbox Pattern
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-4-outbox-pattern>

课程：15. 队列
任务序号：9
短标题：Outbox Pattern
难度：advanced
子主题：Exactly-Once Delivery

## 中文导读

本题要求你完成 `实现 Outbox Pattern`。

重点关注：`outbox pattern`、`event publishing`、`database transactions`、`message reliability`、`eventual consistency`。

建议先按提示逐步实现：Outbox table: Store 消息 in database table。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

**The outbox pattern**:. ```. Problem: Publishing 消息 reliably. Scenario:. 1. Start database 事务. 2. Update business data (create order). 3. Commit 事务. 4. Publish 消息 to 队列. 5. Step 4 fails! (队列 down, 网络 issue). 6. 消息 never published. 7. Order created but no notification sent. Solution: Outbox pattern. 1. Start database 事务. 2. Update business data (create order). 3. Write 消息 to outbox table. 4. Commit 事务 (atomic!). 5. Background process reads outbox. 6. Publishes 消息 to 队列. 7. Marks 消息 as published. Benefits:. - Atomic business data + 消息 creation. - No lost 消息. - Eventually consistent. - 故障-tolerant publishing. ```. **Outbox table structure**:. ```sql. CREATE TABLE outbox (. id BIGSERIAL PRIMARY KEY,. aggregate_type VARCHAR(255) NOT NULL,. aggregate_id VARCHAR(255) NOT NULL,. event_type VARCHAR(255) NOT NULL,. payload JSONB NOT NULL,. created_at TIMESTAMP NOT NULL DEFAULT NOW(),. processed BOOLEAN NOT NULL DEFAULT FALSE,. processed_at TIMESTAMP,. UNIQUE(aggregate_type, aggregate_id, event_type). );. CREATE 索引 idx_outbox_created ON outbox(created_at);. ```. **Outbox 消息 publisher**:. ```typescript. id: number;. aggregateType: string;. aggregateId: string;. eventType: string;. payload: any;. createdAt: Date;. processed: boolean;. processedAt?: Date;. private database: Database;. private messageQueue: MessageQueue;. private pollingIntervalMs = 1000; // 1 second. private batchSize = 100;. this.database = database;. this.messageQueue = messageQueue;. // Start polling用于unprocessed 消息. console.日志('Starting outbox publisher...');. await this.processBatch();. // Process batch of unprocessed 消息. // Get unprocessed 消息. const 消息 = await this.getUnprocessedMessages(this.batchSize);. return;. // Publish each 消息. await this.publishMessage(消息);. console.error('Error processing outbox batch:', error);. // Get unprocessed 消息. const result = await this.database.query(. `SELECT * FROM outbox. WHERE processed = FALSE. ORDER BY created_at ASC. LIMIT $1. FOR UPDATE SKIP LOCKED`,
            [limit]
        );

        return result.rows;
    }

    // Publish single 消息
    private async publishMessage(消息: OutboxMessage): Promise<void> {
        try {
            console.日志(`Publishing outbox 消息 ${消息.id}`);

            // Publish to 消息 队列
            await this.messageQueue.send({
                type: 消息.eventType,
                aggregateType: 消息.aggregateType,
                aggregateId: 消息.aggregateId,
                payload: 消息.payload
            });

            // Mark as processed
            await this.markAsProcessed(消息.id);

            console.日志(`Outbox 消息 ${消息.id} published和marked as processed`);

        } catch (error) {
            console.error(`Failed to publish outbox 消息 ${消息.id}:`, error);

            // Don't mark as processed (will be retried)
        }
    }

    // Mark 消息 as processed
    private async markAsProcessed(messageId: number): Promise<void> {
        await this.database.query(
            `UPDATE outbox
             SET processed = TRUE,
                 processed_at = NOW()
             WHERE id = $1`,
            [messageId]
        );
    }

    // Cleanup old processed 消息
    async cleanup(olderThanHours: number = 24): Promise<void> {
        const cutoff = new Date();
        cutoff.setHours(cutoff.getHours() - olderThanHours);

        const result = await this.database.query(
            `DELETE FROM outbox
             WHERE processed = TRUE
             AND processed_at < $1`,
            [cutoff]
        );

        console.日志(`Cleaned up ${result.rowCount} old outbox 消息`);
    }
}
```

**Outbox 消息 writer**:
```typescript
class OutboxWriter {
    private database: Database;

    constructor(database: Database) {
        this.database = database;
    }

    // Write business data和outbox 消息 atomically
    async writeInTransaction<T>(
        businessData: T,
        events: OutboxEvent[]
    ): Promise<void> {
        await this.database.事务(async (trx) => {
            // Write business data
            await this.writeBusinessData(businessData, trx);

            // Write outbox 消息
           用于(const event of events) {
                await this.writeOutboxMessage(event, trx);
            }
        });

        console.日志(`Business data和${events.length} outbox 消息 written atomically`);
    }

    // Write business data
    private async writeBusinessData<T>(data: T, trx: any): Promise<void> {
        // Implement business data writing
        console.日志('Writing business data:', data);
    }

    // Write outbox 消息
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

**Example: Order creation，包含outbox**:
```typescript
class OrderService {
    private database: Database;
    private outboxWriter: OutboxWriter;

    constructor(database: Database) {
        this.database = database;
        this.outboxWriter = new OutboxWriter(database);
    }

    // Create order，包含events
    async createOrder(orderData: CreateOrderRequest): Promise<Order> {
        console.日志(`Creating order用于user ${orderData.userId}`);

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

        // Write order和events atomically
        await this.outboxWriter.writeInTransaction(order, events);

        console.日志(`Order ${order.id} created，包含${events.length} events`);

        return order;
    }
}
```

**Idempotent outbox processing**:
```typescript
class IdempotentOutboxPublisher extends OutboxPublisher {
    private publishedMessageIds: Set<string> = new Set();

    // Override publish to add idempotency
    protected async publishMessage(消息: OutboxMessage): Promise<void> {
        // Check if already published
        const messageKey = `${消息.aggregateType}:${消息.aggregateId}:${消息.eventType}`;

        if (this.publishedMessageIds.has(messageKey)) {
            console.日志(`消息 ${messageKey} already published, skipping`);

            await this.markAsProcessed(消息.id);

            return;
        }

        // Publish 消息
        await super.publishMessage(消息);

        // Mark as published
        this.publishedMessageIds.add(messageKey);
    }

    // Cleanup published 消息 IDs
    cleanupPublishedIds(olderThanHours: number = 1): void {
        const cutoff = Date.now() - (olderThanHours * 60 * 60 * 1000);

        // This would need to be implemented based on your tracking mechanism
        console.日志(`Cleanup published IDs older than ${olderThanHours} hours`);
    }
}
```

**Transactional outbox，包含Kafka**:
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
        const 消息 = await this.getUnprocessedMessages(100);

       用于(const 消息 of 消息) {
            try {
                // Send to Kafka
                await this.kafkaProducer.send({
                    topic: this.topic,
                    key: 消息.aggregateId,
                    value: JSON.stringify({
                        type: 消息.eventType,
                        aggregateType: 消息.aggregateType,
                        aggregateId: 消息.aggregateId,
                        payload: 消息.payload
                    })
                });

                // Mark as processed
                await this.markAsProcessed(消息.id);

                console.日志(`Outbox 消息 ${消息.id} sent to Kafka`);

            } catch (error) {
                console.error(`Failed to send to Kafka:`, error);

                // Don't mark as processed (will 重试)
            }
        }
    }
}
```

**Example outbox flow**:
```typescript
// Create order，包含outbox
const orderService = new OrderService(database);

await orderService.createOrder({
    userId: 'user-123',
    items: [
        { productId: 'prod-1', quantity: 2 },
        { productId: 'prod-2', quantity: 1 }
    ]
});

// Output:
// Creating order用于user user-123
// Business data和2 outbox 消息 written atomically
// Order order-123 created，包含2 events

// Background outbox publisher processes events:
// Processing 2 outbox 消息
// Publishing outbox 消息 1
// Published OrderCreated event用于order order-123
// Publishing outbox 消息 2
// Published PaymentRequested event用于order order-123
// Outbox 消息 1 published和marked as processed
// Outbox 消息 2 published和marked as processed
```

**Example outbox scenarios**:
```JSON
// Scenario 1: Atomic write
{
  "事务": [
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

- Outbox table: Store 消息 in database table
- Atomic write: Write business data + outbox 消息 in one 事务
- Separate publisher: Background process reads outbox和publishes
- Idempotent publishing: Track published 消息 to avoid duplicates
- Cleanup: Delete published 消息 after confirmation

## 测试用例

### 1. Write to outbox atomically

Should write business data和outbox events atomically.

输入：

```json
{"src":"service","dest":"outbox","body":{"type":"write","msg_id":1,"business_data":{"order_id":"order-123"},"events":[{"type":"OrderCreated"},{"type":"PaymentRequested"}]}}
```

期望输出：

```text
{"type": "written", "in_reply_to": 1, "order_id": "order-123", "outbox_events": 2}
```

### 2. Publish outbox messages

Should publish outbox 消息 to 队列.

输入：

```json
{"src":"publisher","dest":"queue","body":{"type":"publish","msg_id":1,"outbox_messages":[{"id":1,"event_type":"OrderCreated","payload":{"order_id":"order-123"}}]}}
```

期望输出：

```text
{"type": "published", "in_reply_to": 1, "published_count": 1, "marked_processed": true}
```

## 参考资料

- [Outbox Pattern](https://www.eventstore.com/blog/event-sourcing-with-the-outbox-pattern/)：Outbox pattern用于reliable publishing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
