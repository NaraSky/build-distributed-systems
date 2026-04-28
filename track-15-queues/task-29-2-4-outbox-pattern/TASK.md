# Implement Outbox Pattern

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-4-outbox-pattern>

Track: 15. Queues
Task order: 9
Short title: Outbox Pattern
Difficulty: advanced
Subtrack: Exactly-Once Delivery

## Problem

**The outbox pattern**:. ```. Problem: Publishing messages reliably. Scenario:. 1. Start database transaction. 2. Update business data (create order). 3. Commit transaction. 4. Publish message to queue. 5. Step 4 fails! (queue down, network issue). 6. Message never published. 7. Order created but no notification sent. Solution: Outbox pattern. 1. Start database transaction. 2. Update business data (create order). 3. Write message to outbox table. 4. Commit transaction (atomic!). 5. Background process reads outbox. 6. Publishes message to queue. 7. Marks message as published. Benefits:. - Atomic business data + message creation. - No lost messages. - Eventually consistent. - Fault-tolerant publishing. ```. **Outbox table structure**:. ```sql. CREATE TABLE outbox (. id BIGSERIAL PRIMARY KEY,. aggregate_type VARCHAR(255) NOT NULL,. aggregate_id VARCHAR(255) NOT NULL,. event_type VARCHAR(255) NOT NULL,. payload JSONB NOT NULL,. created_at TIMESTAMP NOT NULL DEFAULT NOW(),. processed BOOLEAN NOT NULL DEFAULT FALSE,. processed_at TIMESTAMP,. UNIQUE(aggregate_type, aggregate_id, event_type). );. CREATE INDEX idx_outbox_created ON outbox(created_at);. ```. **Outbox message publisher**:. ```typescript. id: number;. aggregateType: string;. aggregateId: string;. eventType: string;. payload: any;. createdAt: Date;. processed: boolean;. processedAt?: Date;. private database: Database;. private messageQueue: MessageQueue;. private pollingIntervalMs = 1000; // 1 second. private batchSize = 100;. this.database = database;. this.messageQueue = messageQueue;. // Start polling for unprocessed messages. console.log('Starting outbox publisher...');. await this.processBatch();. // Process batch of unprocessed messages. // Get unprocessed messages. const messages = await this.getUnprocessedMessages(this.batchSize);. return;. // Publish each message. await this.publishMessage(message);. console.error('Error processing outbox batch:', error);. // Get unprocessed messages. const result = await this.database.query(. `SELECT * FROM outbox. WHERE processed = FALSE. ORDER BY created_at ASC. LIMIT $1. FOR UPDATE SKIP LOCKED`,
            [limit]
        );

        return result.rows;
    }

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
}
```

**Outbox message writer**:
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
    private async writeBusinessData<T>(data: T, trx: any): Promise<void> {
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

**Example: Order creation with outbox**:
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

**Idempotent outbox processing**:
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

**Transactional outbox with Kafka**:
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

**Example outbox flow**:
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

**Example outbox scenarios**:
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

## Concepts

- outbox pattern
- event publishing
- database transactions
- message reliability
- eventual consistency
- publisher reliability

## Hints

- Outbox table: Store messages in database table
- Atomic write: Write business data + outbox messages in one transaction
- Separate publisher: Background process reads outbox and publishes
- Idempotent publishing: Track published messages to avoid duplicates
- Cleanup: Delete published messages after confirmation

## Test Cases

### 1. Write to outbox atomically

Should write business data and outbox events atomically.

Input:

```json
{"src":"service","dest":"outbox","body":{"type":"write","msg_id":1,"business_data":{"order_id":"order-123"},"events":[{"type":"OrderCreated"},{"type":"PaymentRequested"}]}}
```

Expected output:

```text
{"type": "written", "in_reply_to": 1, "order_id": "order-123", "outbox_events": 2}
```

### 2. Publish outbox messages

Should publish outbox messages to queue.

Input:

```json
{"src":"publisher","dest":"queue","body":{"type":"publish","msg_id":1,"outbox_messages":[{"id":1,"event_type":"OrderCreated","payload":{"order_id":"order-123"}}]}}
```

Expected output:

```text
{"type": "published", "in_reply_to": 1, "published_count": 1, "marked_processed": true}
```

## Resources

- [Outbox Pattern](https://www.eventstore.com/blog/event-sourcing-with-the-outbox-pattern/): Outbox pattern for reliable publishing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
