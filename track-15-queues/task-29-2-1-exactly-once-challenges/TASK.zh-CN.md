# Understand Exactly-Once Delivery Challenges

英文标题：Understand Exactly-Once Delivery Challenges
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-1-exactly-once-challenges>

课程：15. 队列
任务序号：6
短标题：Exactly-Once Challenges
难度：intermediate
子主题：Exactly-Once Delivery

## 中文导读

本题要求你完成 `Understand Exactly-Once Delivery Challenges`。

重点关注：`exactly-once semantics`、`message delivery`、`idempotency`、`at-least-once`、`at-most-once`。

建议先按提示逐步实现：Producer retries: 网络 failures can cause duplicate sends。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

**The exactly-once challenge**:. ```. Problem: 分布式系统 make guarantees hard. Scenario 1: Producer 重试. 1. Producer sends 消息 to 队列. 2. 队列 stores 消息. 3. ACK lost in 网络. 4. Producer retries (thinks send failed). 5. 队列 now has duplicate 消息. Scenario 2: Consumer crash. 1. Consumer receives 消息. 2. Consumer processes 消息. 3. Consumer crashes before ACK. 4. 队列 re-delivers 消息. 5. Consumer processes same 消息 again. Result: Duplicates break business logic. - Payment processed twice. - Inventory decremented twice. - Email sent twice. Solution: Exactly-once semantics. - Each 消息 processed exactly once. - No duplicates, no data loss. - Requires coordination across components. ```. **Delivery semantics**:. ```typescript. // At-most-once (fire和forget). // Send without waiting用于ACK. this.队列.send(消息);. console.日志('消息 sent (no confirmation)');. // At-least-once (ACK + 重试). let sent = false;. await this.队列.sendWithAck(消息);. sent = true;. console.日志('消息 sent和acknowledged');. console.日志('Send failed, retrying...');. await this.sleep(1000);. return new Promise(resolve => setTimeout(resolve, ms));. // Exactly-once (idempotent + deduplication). private sentMessages: Set<string> = new Set();. // Check if already sent. return;. // Send，包含ACK和重试. let sent = false;. await this.队列.sendWithAck(消息);. this.sentMessages.add(消息.id);. sent = true;. console.日志('Send failed, retrying...');. await this.sleep(1000);. ```. **Consumer processing challenges**:. ```typescript. // Problematic consumer (not idempotent). private processed = false;. // Process 消息. this.decrementInventory(消息.product);. this.processed = true;. // Simulate crash before ACK. console.日志('Consumer crashing before ACK...');. throw new Error('Consumer crashed');. // ACK 消息. await this.队列.ack(消息.id);. // This will be called multiple times on retries!. // Idempotent consumer. private processedMessages: Set<string> = new Set();. // Check if already processed. // Still need to ACK. await this.队列.ack(消息.id);. return;. // Process 消息. this.decrementInventory(消息.product);. this.processedMessages.add(消息.id);. // Simulate potential crash. console.日志('Consumer crashing before ACK...');. throw new Error('Consumer crashed');. // ACK 消息. await this.队列.ack(消息.id);. ```. **故障 scenarios**:. ```typescript. // Scenario 1: Producer 重试 due to lost ACK. console.日志('=== Producer 重试 Scenario ===');. // First send attempt. console.日志('Producer: Sending 消息...');. await this.队列.send(消息);. console.日志('队列: 消息 received');. // ACK lost. console.日志('网络: ACK lost!');. // Producer retries. console.日志('Producer: No ACK received, retrying...');. await this.队列.send(消息);. console.日志('队列: Duplicate 消息 received!');. console.日志('Result: 队列 has duplicate 消息');. // Scenario 2: Consumer crash before ACK. console.日志('=== Consumer Crash Scenario ===');. console.日志('Consumer: Receiving 消息...');. // Process 消息. console.日志('Consumer: Processing 消息...');. console.日志('Consumer: Inventory decremented');. // Crash before ACK. console.日志('Consumer: Crashing before ACK!');. console.日志('Consumer: State lost');. // 队列 re-delivers. console.日志('队列: No ACK received, re-delivering...');. console.日志('Consumer: Receiving 消息 again...');. console.日志('Consumer: Processing 消息 again...');. console.日志('Consumer: Inventory decremented again!');. console.日志('Result: Inventory decremented twice');. // Scenario 3: 网络 partition. console.日志('=== 网络 Partition Scenario ===');. console.日志('Producer: Sending 消息...');. // 消息 sent but 队列 is partitioned. console.日志('网络: Partition occurred!');. // Producer times out. console.日志('Producer: 超时, retrying...');. await this.队列.send(消息);. // Partition heals. console.日志('网络: Partition healed');. console.日志('队列: Both 消息 received');. console.日志('Result: Duplicate 消息 in 队列');. ```. **Exactly-once requirements**:. ```typescript. // Producer side. producerDeduplication: boolean; // Detect和skip duplicate sends. // 队列 side. duplicateDetection: boolean; // 队列 detects duplicate 消息 IDs. exactlyOnceSemantics: boolean; // 队列 provides exactly-once guarantees. // Consumer side. consumerDeduplication: boolean; // Track processed 消息 IDs. atomicProcessing: boolean; // Process + ACK in single 事务. // Coordination. transactionSupport: boolean; // 队列 + DB in same 事务. twoPhaseCommit: boolean; // Distributed 事务 coordination. const issues: string[] = [];. // Producer requirements. issues.push('Producer must be idempotent');. issues.push('Producer needs deduplication');. // Consumer requirements. issues.push('Consumer must be idempotent');. issues.push('Consumer needs deduplication');. issues.push('Consumer needs atomic processing');. // Coordination requirements. issues.push('Need 事务 support or 2PC');. return 'System can achieve exactly-once semantics';. ```. **Example 故障 scenarios**:. ```JSON. // Scenario 1: Producer 重试. "scenario": "producer_retry",. "steps": [. ],. "result": "duplicate_messages". // Scenario 2: Consumer crash. "scenario": "consumer_crash",. "steps": [. ],. "result": "duplicate_processing". ```

## 涉及概念

- `exactly-once semantics`
- `message delivery`
- `idempotency`
- `at-least-once`
- `at-most-once`
- `duplicate processing`

## 实现提示

- Producer retries: 网络 failures can cause duplicate sends
- Consumer crashes: Can reprocess 消息 after recovery
- 网络 issues: Lost acknowledgments cause retransmission
- Exactly-once requires: Idempotent producers + Idempotent consumers
- Trade-offs: Exactly-once requires coordination和overhead

## 测试用例

### 1. Detect duplicate 消息

Should detect和reject duplicate 消息.

输入：

```json
{"src":"producer","dest":"queue","body":{"type":"send","msg_id":1,"message":{"id":"msg-1"}}}
```

期望输出：

```text
{"type": "duplicate_detected", "in_reply_to": 1, "message_id": "msg-1", "action": "rejected"}
```

### 2.处理lost ACK

Should handle lost ACK和重试.

输入：

```json
{"src":"producer","dest":"network","body":{"type":"send_with_ack","msg_id":1,"message":{"id":"msg-1"},"ack_lost":true}}
```

期望输出：

```text
{"type": "ack_lost", "in_reply_to": 1, "message_id": "msg-1", "action": "retry"}
```

## 参考资料

- [Exactly-Once Delivery](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)：Kafka exactly-once semantics

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
