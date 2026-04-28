# Understand Exactly-Once Delivery Challenges

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-1-exactly-once-challenges>

Track: 15. Queues
Task order: 6
Short title: Exactly-Once Challenges
Difficulty: intermediate
Subtrack: Exactly-Once Delivery

## Problem

**The exactly-once challenge**:. ```. Problem: Distributed systems make guarantees hard. Scenario 1: Producer retry. 1. Producer sends message to queue. 2. Queue stores message. 3. ACK lost in network. 4. Producer retries (thinks send failed). 5. Queue now has duplicate message. Scenario 2: Consumer crash. 1. Consumer receives message. 2. Consumer processes message. 3. Consumer crashes before ACK. 4. Queue re-delivers message. 5. Consumer processes same message again. Result: Duplicates break business logic. - Payment processed twice. - Inventory decremented twice. - Email sent twice. Solution: Exactly-once semantics. - Each message processed exactly once. - No duplicates, no data loss. - Requires coordination across components. ```. **Delivery semantics**:. ```typescript. // At-most-once (fire and forget). // Send without waiting for ACK. this.queue.send(message);. console.log('Message sent (no confirmation)');. // At-least-once (ACK + retry). let sent = false;. await this.queue.sendWithAck(message);. sent = true;. console.log('Message sent and acknowledged');. console.log('Send failed, retrying...');. await this.sleep(1000);. return new Promise(resolve => setTimeout(resolve, ms));. // Exactly-once (idempotent + deduplication). private sentMessages: Set<string> = new Set();. // Check if already sent. return;. // Send with ACK and retry. let sent = false;. await this.queue.sendWithAck(message);. this.sentMessages.add(message.id);. sent = true;. console.log('Send failed, retrying...');. await this.sleep(1000);. ```. **Consumer processing challenges**:. ```typescript. // Problematic consumer (not idempotent). private processed = false;. // Process message. this.decrementInventory(message.product);. this.processed = true;. // Simulate crash before ACK. console.log('Consumer crashing before ACK...');. throw new Error('Consumer crashed');. // ACK message. await this.queue.ack(message.id);. // This will be called multiple times on retries!. // Idempotent consumer. private processedMessages: Set<string> = new Set();. // Check if already processed. // Still need to ACK. await this.queue.ack(message.id);. return;. // Process message. this.decrementInventory(message.product);. this.processedMessages.add(message.id);. // Simulate potential crash. console.log('Consumer crashing before ACK...');. throw new Error('Consumer crashed');. // ACK message. await this.queue.ack(message.id);. ```. **Failure scenarios**:. ```typescript. // Scenario 1: Producer retry due to lost ACK. console.log('=== Producer Retry Scenario ===');. // First send attempt. console.log('Producer: Sending message...');. await this.queue.send(message);. console.log('Queue: Message received');. // ACK lost. console.log('Network: ACK lost!');. // Producer retries. console.log('Producer: No ACK received, retrying...');. await this.queue.send(message);. console.log('Queue: Duplicate message received!');. console.log('Result: Queue has duplicate messages');. // Scenario 2: Consumer crash before ACK. console.log('=== Consumer Crash Scenario ===');. console.log('Consumer: Receiving message...');. // Process message. console.log('Consumer: Processing message...');. console.log('Consumer: Inventory decremented');. // Crash before ACK. console.log('Consumer: Crashing before ACK!');. console.log('Consumer: State lost');. // Queue re-delivers. console.log('Queue: No ACK received, re-delivering...');. console.log('Consumer: Receiving message again...');. console.log('Consumer: Processing message again...');. console.log('Consumer: Inventory decremented again!');. console.log('Result: Inventory decremented twice');. // Scenario 3: Network partition. console.log('=== Network Partition Scenario ===');. console.log('Producer: Sending message...');. // Message sent but queue is partitioned. console.log('Network: Partition occurred!');. // Producer times out. console.log('Producer: Timeout, retrying...');. await this.queue.send(message);. // Partition heals. console.log('Network: Partition healed');. console.log('Queue: Both messages received');. console.log('Result: Duplicate messages in queue');. ```. **Exactly-once requirements**:. ```typescript. // Producer side. producerDeduplication: boolean; // Detect and skip duplicate sends. // Queue side. duplicateDetection: boolean; // Queue detects duplicate message IDs. exactlyOnceSemantics: boolean; // Queue provides exactly-once guarantees. // Consumer side. consumerDeduplication: boolean; // Track processed message IDs. atomicProcessing: boolean; // Process + ACK in single transaction. // Coordination. transactionSupport: boolean; // Queue + DB in same transaction. twoPhaseCommit: boolean; // Distributed transaction coordination. const issues: string[] = [];. // Producer requirements. issues.push('Producer must be idempotent');. issues.push('Producer needs deduplication');. // Consumer requirements. issues.push('Consumer must be idempotent');. issues.push('Consumer needs deduplication');. issues.push('Consumer needs atomic processing');. // Coordination requirements. issues.push('Need transaction support or 2PC');. return 'System can achieve exactly-once semantics';. ```. **Example failure scenarios**:. ```json. // Scenario 1: Producer retry. "scenario": "producer_retry",. "steps": [. ],. "result": "duplicate_messages". // Scenario 2: Consumer crash. "scenario": "consumer_crash",. "steps": [. ],. "result": "duplicate_processing". ```

## Concepts

- exactly-once semantics
- message delivery
- idempotency
- at-least-once
- at-most-once
- duplicate processing

## Hints

- Producer retries: Network failures can cause duplicate sends
- Consumer crashes: Can reprocess messages after recovery
- Network issues: Lost acknowledgments cause retransmission
- Exactly-once requires: Idempotent producers + Idempotent consumers
- Trade-offs: Exactly-once requires coordination and overhead

## Test Cases

### 1. Detect duplicate message

Should detect and reject duplicate messages.

Input:

```json
{"src":"producer","dest":"queue","body":{"type":"send","msg_id":1,"message":{"id":"msg-1"}}}
```

Expected output:

```text
{"type": "duplicate_detected", "in_reply_to": 1, "message_id": "msg-1", "action": "rejected"}
```

### 2. Handle lost ACK

Should handle lost ACK and retry.

Input:

```json
{"src":"producer","dest":"network","body":{"type":"send_with_ack","msg_id":1,"message":{"id":"msg-1"},"ack_lost":true}}
```

Expected output:

```text
{"type": "ack_lost", "in_reply_to": 1, "message_id": "msg-1", "action": "retry"}
```

## Resources

- [Exactly-Once Delivery](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/): Kafka exactly-once semantics

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
