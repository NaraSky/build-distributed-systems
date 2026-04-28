# 理解精确一次投递的挑战

英文标题：Understand Exactly-Once Delivery Challenges
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-1-exactly-once-challenges>

课程：15. 队列
任务序号：6
短标题：精确一次的挑战
难度：进阶
子主题：精确一次投递

## 中文导读

本题带你深入理解为什么"精确一次投递"在分布式系统中如此困难。通过分析生产者重试导致的重复发送、消费者崩溃导致的重复处理等典型场景，你将理解各种投递语义的区别，以及实现精确一次所需要的条件。这是后续实现幂等消费者、事务处理等进阶模式的理论基础。

## 题目说明

**精确一次的挑战**：

分布式系统中，提供可靠的投递保证非常困难。以下是两个典型的问题场景：

场景一：生产者重试
1. 生产者向队列发送消息
2. 队列成功存储了消息
3. 确认（ACK）在网络传输中丢失
4. 生产者以为发送失败，于是重试
5. 队列中出现了重复的消息

场景二：消费者崩溃
1. 消费者接收到消息
2. 消费者处理了消息
3. 消费者在发送确认之前崩溃
4. 队列重新投递该消息
5. 消费者再次处理同一条消息

重复处理会导致严重的业务问题：付款扣了两次、库存减了两遍、邮件发了两封。

解决方案就是精确一次语义（Exactly-Once Semantics）：每条消息恰好被处理一次，没有重复，也没有丢失，但这需要多个组件之间的协调配合。

**投递语义**：

```typescript
// At-most-once (fire and forget)
// Send without waiting for ACK
this.queue.send(message);
console.log('Message sent (no confirmation)');

// At-least-once (ACK + retry)
let sent = false;
await this.queue.sendWithAck(message);
sent = true;
console.log('Message sent and acknowledged');
console.log('Send failed, retrying...');
await this.sleep(1000);
return new Promise(resolve => setTimeout(resolve, ms));

// Exactly-once (idempotent + deduplication)
private sentMessages: Set<string> = new Set();
// Check if already sent
return;
// Send with ACK and retry
let sent = false;
await this.queue.sendWithAck(message);
this.sentMessages.add(message.id);
sent = true;
console.log('Send failed, retrying...');
await this.sleep(1000);
```

**消费者处理的挑战**：

```typescript
// Problematic consumer (not idempotent)
private processed = false;
// Process message
this.decrementInventory(message.product);
this.processed = true;
// Simulate crash before ACK
console.log('Consumer crashing before ACK...');
throw new Error('Consumer crashed');
// ACK message
await this.queue.ack(message.id);
// This will be called multiple times on retries!

// Idempotent consumer
private processedMessages: Set<string> = new Set();
// Check if already processed
// Still need to ACK
await this.queue.ack(message.id);
return;
// Process message
this.decrementInventory(message.product);
this.processedMessages.add(message.id);
// Simulate potential crash
console.log('Consumer crashing before ACK...');
throw new Error('Consumer crashed');
// ACK message
await this.queue.ack(message.id);
```

**故障场景**：

```typescript
// Scenario 1: Producer retry due to lost ACK
console.log('=== Producer Retry Scenario ===');
// First send attempt
console.log('Producer: Sending message...');
await this.queue.send(message);
console.log('Queue: Message received');
// ACK lost
console.log('Network: ACK lost!');
// Producer retries
console.log('Producer: No ACK received, retrying...');
await this.queue.send(message);
console.log('Queue: Duplicate message received!');
console.log('Result: Queue has duplicate messages');

// Scenario 2: Consumer crash before ACK
console.log('=== Consumer Crash Scenario ===');
console.log('Consumer: Receiving message...');
// Process message
console.log('Consumer: Processing message...');
console.log('Consumer: Inventory decremented');
// Crash before ACK
console.log('Consumer: Crashing before ACK!');
console.log('Consumer: State lost');
// Queue re-delivers
console.log('Queue: No ACK received, re-delivering...');
console.log('Consumer: Receiving message again...');
console.log('Consumer: Processing message again...');
console.log('Consumer: Inventory decremented again!');
console.log('Result: Inventory decremented twice');

// Scenario 3: Network partition
console.log('=== Network Partition Scenario ===');
console.log('Producer: Sending message...');
// Message sent but queue is partitioned
console.log('Network: Partition occurred!');
// Producer times out
console.log('Producer: Timeout, retrying...');
await this.queue.send(message);
// Partition heals
console.log('Network: Partition healed');
console.log('Queue: Both messages received');
console.log('Result: Duplicate messages in queue');
```

**精确一次的必要条件**：

```typescript
// Producer side
producerDeduplication: boolean; // Detect and skip duplicate sends
// Queue side
duplicateDetection: boolean; // Queue detects duplicate message IDs
exactlyOnceSemantics: boolean; // Queue provides exactly-once guarantees
// Consumer side
consumerDeduplication: boolean; // Track processed message IDs
atomicProcessing: boolean; // Process + ACK in single transaction
// Coordination
transactionSupport: boolean; // Queue + DB in same transaction
twoPhaseCommit: boolean; // Distributed transaction coordination
const issues: string[] = [];
// Producer requirements
issues.push('Producer must be idempotent');
issues.push('Producer needs deduplication');
// Consumer requirements
issues.push('Consumer must be idempotent');
issues.push('Consumer needs deduplication');
issues.push('Consumer needs atomic processing');
// Coordination requirements
issues.push('Need transaction support or 2PC');
return 'System can achieve exactly-once semantics';
```

**故障场景示例**：

```json
// Scenario 1: Producer retry
"scenario": "producer_retry",
"steps": [
],
"result": "duplicate_messages"

// Scenario 2: Consumer crash
"scenario": "consumer_crash",
"steps": [
],
"result": "duplicate_processing"
```

## 涉及概念

- `exactly-once semantics`
- `message delivery`
- `idempotency`
- `at-least-once`
- `at-most-once`
- `duplicate processing`

## 实现提示

- 生产者重试：网络故障可能导致重复发送
- 消费者崩溃：恢复后可能重复处理消息
- 网络问题：确认丢失会触发重新传输
- 精确一次需要：幂等的生产者 + 幂等的消费者
- 权衡取舍：精确一次需要额外的协调开销

## 测试用例

### 1. 检测重复消息

应当能够检测并拒绝重复的消息。

输入：

```json
{"src":"producer","dest":"queue","body":{"type":"send","msg_id":1,"message":{"id":"msg-1"}}}
```

期望输出：

```text
{"type": "duplicate_detected", "in_reply_to": 1, "message_id": "msg-1", "action": "rejected"}
```

### 2. 处理确认丢失

应当能够处理确认丢失并触发重试。

输入：

```json
{"src":"producer","dest":"network","body":{"type":"send_with_ack","msg_id":1,"message":{"id":"msg-1"},"ack_lost":true}}
```

期望输出：

```text
{"type": "ack_lost", "in_reply_to": 1, "message_id": "msg-1", "action": "retry"}
```

## 参考资料

- [Exactly-Once Delivery](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)：Kafka 精确一次语义的实现原理

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
