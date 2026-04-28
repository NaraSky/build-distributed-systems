# 实现队列与数据库的两阶段提交

英文标题：Implement Two-Phase Commit for Queue and Database
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-5-two-phase-commit>

课程：15. 队列
任务序号：10
短标题：两阶段提交
难度：高级
子主题：精确一次投递

## 中文导读

本题要求你实现两阶段提交（Two-Phase Commit，简称 2PC），用来协调队列和数据库之间的原子提交。两阶段提交就像婚礼上的宣誓——牧师先问双方"你愿意吗"（准备阶段），只有双方都说"我愿意"才正式宣布结婚（提交阶段），只要有一方说"不"就取消（回滚阶段）。这是分布式事务最经典的协调协议。

## 题目说明

两阶段提交（2PC）协调多个分布式系统之间的原子提交，确保所有参与者要么全部提交，要么全部回滚。

**要解决的问题**：如何协调队列和数据库的提交。典型问题场景：
1. 消费者接收到消息
2. 消费者更新了数据库
3. 消费者提交了数据库事务
4. 消费者在发送确认之前崩溃
5. 队列重新投递消息
6. 数据库已经更新过了，导致重复操作

解决方案就是两阶段提交。

**第一阶段 - 准备**：队列准备确认消息，数据库准备提交事务，双方各自投票"同意"或"拒绝"。

**第二阶段 - 提交或回滚**：如果双方都投了"同意"，则全部提交；如果任何一方投了"拒绝"，则全部回滚。

**优势**：跨系统的原子提交、不会出现部分更新、实现精确一次语义、容错的协调机制。

**两阶段提交协调器**：

```typescript
interface Participant {
    id: string;
    prepare(transactionId: string): Promise<boolean>;
    commit(transactionId: string): Promise<void>;
    rollback(transactionId: string): Promise<void>;
}

class TwoPhaseCommitCoordinator {
    private participants: Map<string, Participant> = new Map();
    private transactions: Map<string, TransactionState> = new Map();
    private timeoutMs = 30000; // 30 seconds

    // Register participant
    registerParticipant(participant: Participant): void {
        this.participants.set(participant.id, participant);
    }

    // Execute distributed transaction
    async executeTransaction(
        transactionId: string,
        operations: Map<string, () => Promise<void>>
    ): Promise<boolean> {
        // Initialize transaction state
        const state: TransactionState = {
            id: transactionId,
            status: 'pending',
            participants: Array.from(this.participants.keys()),
            votes: new Map()
        };
        this.transactions.set(transactionId, state);

        // Phase 1: Prepare
        const prepared = await this.preparePhase(transactionId, operations);

        if (!prepared) {
            // Prepare failed, rollback
            await this.rollbackPhase(transactionId);
            return false;
        }

        // Phase 2: Commit
        await this.commitPhase(transactionId);
        return true;
    }

    // Phase 1: Prepare
    private async preparePhase(
        transactionId: string,
        operations: Map<string, () => Promise<void>>
    ): Promise<boolean> {
        console.log(`Transaction ${transactionId}: Prepare phase`);

        const state = this.transactions.get(transactionId)!;
        state.status = 'preparing';

        // Prepare all participants
        for (const [participantId, participant] of this.participants) {
            try {
                console.log(`Preparing participant ${participantId}`);

                // Execute prepare operation
                const operation = operations.get(participantId);

                if (operation) {
                    await operation();
                }

                // Ask participant to prepare
                const vote = await participant.prepare(transactionId);

                state.votes.set(participantId, vote);

                if (!vote) {
                    console.log(`Participant ${participantId} voted NO`);
                    state.status = 'prepare_failed';
                    return false;
                }

                console.log(`Participant ${participantId} voted YES`);

            } catch (error) {
                console.error(`Participant ${participantId} prepare failed:`, error);
                state.votes.set(participantId, false);
                state.status = 'prepare_failed';
                return false;
            }
        }

        state.status = 'prepared';
        console.log(`Transaction ${transactionId}: All participants voted YES`);
        return true;
    }

    // Phase 2: Commit
    private async commitPhase(transactionId: string): Promise<void> {
        console.log(`Transaction ${transactionId}: Commit phase`);

        const state = this.transactions.get(transactionId)!;
        state.status = 'committing';

        // Commit all participants
        for (const [participantId, participant] of this.participants) {
            try {
                console.log(`Committing participant ${participantId}`);
                await participant.commit(transactionId);
                console.log(`Participant ${participantId} committed`);
            } catch (error) {
                console.error(`Participant ${participantId} commit failed:`, error);
                // Note: In real 2PC, commit failures require recovery
            }
        }

        state.status = 'committed';
        console.log(`Transaction ${transactionId}: Committed`);

        // Cleanup
        this.transactions.delete(transactionId);
    }

    // Rollback phase
    private async rollbackPhase(transactionId: string): Promise<void> {
        console.log(`Transaction ${transactionId}: Rollback phase`);

        const state = this.transactions.get(transactionId)!;
        state.status = 'rolling_back';

        // Rollback all participants
        for (const [participantId, participant] of this.participants) {
            try {
                // Only rollback participants that voted YES
                if (state.votes.get(participantId) === true) {
                    console.log(`Rolling back participant ${participantId}`);
                    await participant.rollback(transactionId);
                    console.log(`Participant ${participantId} rolled back`);
                }
            } catch (error) {
                console.error(`Participant ${participantId} rollback failed:`, error);
            }
        }

        state.status = 'rolled_back';
        console.log(`Transaction ${transactionId}: Rolled back`);

        // Cleanup
        this.transactions.delete(transactionId);
    }
}

interface TransactionState {
    id: string;
    status: 'pending' | 'preparing' | 'prepared' | 'committing' | 'committed' | 'rolling_back' | 'rolled_back' | 'prepare_failed';
    participants: string[];
    votes: Map<string, boolean>;
}
```

**队列参与者**：

```typescript
class QueueParticipant implements Participant {
    id = 'queue';
    private queue: MessageQueue;
    private preparedMessages: Map<string, Message> = new Map();

    constructor(queue: MessageQueue) {
        this.queue = queue;
    }

    // Prepare to ACK message
    async prepare(transactionId: string): Promise<boolean> {
        console.log(`Queue: Prepare for transaction ${transactionId}`);

        try {
            // Check if message exists and can be ACKed
            const message = this.preparedMessages.get(transactionId);

            if (!message) {
                console.log(`Queue: No message for transaction ${transactionId}`);
                return false;
            }

            // Reserve message (don't ACK yet)
            console.log(`Queue: Message reserved for transaction ${transactionId}`);
            return true;

        } catch (error) {
            console.error(`Queue: Prepare failed for transaction ${transactionId}:`, error);
            return false;
        }
    }

    // Commit ACK
    async commit(transactionId: string): Promise<void> {
        console.log(`Queue: Commit for transaction ${transactionId}`);

        const message = this.preparedMessages.get(transactionId);

        if (message) {
            // ACK the message
            await this.queue.ack(message.id, message.offset);
            console.log(`Queue: Message ${message.id} ACKed`);
            this.preparedMessages.delete(transactionId);
        }
    }

    // Rollback (release reservation)
    async rollback(transactionId: string): Promise<void> {
        console.log(`Queue: Rollback for transaction ${transactionId}`);

        // Release message (will be re-delivered)
        this.preparedMessages.delete(transactionId);
        console.log(`Queue: Message released for transaction ${transactionId}`);
    }

    // Prepare message for transaction
    prepareMessage(transactionId: string, message: Message): void {
        this.preparedMessages.set(transactionId, message);
        console.log(`Queue: Message prepared for transaction ${transactionId}`);
    }
}
```

**数据库参与者**：

```typescript
class DatabaseParticipant implements Participant {
    id = 'database';
    private database: Database;
    private transactions: Map<string, DatabaseTransaction> = new Map();

    constructor(database: Database) {
        this.database = database;
    }

    // Prepare transaction
    async prepare(transactionId: string): Promise<boolean> {
        console.log(`Database: Prepare for transaction ${transactionId}`);

        try {
            // Start transaction
            const trx = await this.database.beginTransaction();

            // Store transaction for later commit/rollback
            this.transactions.set(transactionId, trx);

            console.log(`Database: Transaction prepared for ${transactionId}`);
            return true;

        } catch (error) {
            console.error(`Database: Prepare failed for transaction ${transactionId}:`, error);
            return false;
        }
    }

    // Commit transaction
    async commit(transactionId: string): Promise<void> {
        console.log(`Database: Commit for transaction ${transactionId}`);

        const trx = this.transactions.get(transactionId);

        if (trx) {
            await trx.commit();
            this.transactions.delete(transactionId);
            console.log(`Database: Transaction ${transactionId} committed`);
        }
    }

    // Rollback transaction
    async rollback(transactionId: string): Promise<void> {
        console.log(`Database: Rollback for transaction ${transactionId}`);

        const trx = this.transactions.get(transactionId);

        if (trx) {
            await trx.rollback();
            this.transactions.delete(transactionId);
            console.log(`Database: Transaction ${transactionId} rolled back`);
        }
    }

    // Get transaction for operations
    getTransaction(transactionId: string): DatabaseTransaction | undefined {
        return this.transactions.get(transactionId);
    }
}
```

**结合两阶段提交的精确一次消费者**：

```typescript
class ExactlyOnceConsumerWith2PC {
    private coordinator: TwoPhaseCommitCoordinator;
    private queueParticipant: QueueParticipant;
    private databaseParticipant: DatabaseParticipant;

    constructor(queue: MessageQueue, database: Database) {
        this.coordinator = new TwoPhaseCommitCoordinator();
        this.queueParticipant = new QueueParticipant(queue);
        this.databaseParticipant = new DatabaseParticipant(database);

        // Register participants
        this.coordinator.registerParticipant(this.queueParticipant);
        this.coordinator.registerParticipant(this.databaseParticipant);
    }

    // Consume message with exactly-once semantics
    async consume(message: Message): Promise<boolean> {
        const transactionId = `tx-${message.id}`;
        console.log(`Processing message ${message.id} with 2PC`);

        // Prepare queue participant
        this.queueParticipant.prepareMessage(transactionId, message);

        // Define transaction operations
        const operations = new Map<string, () => Promise<void>>();

        // Database operation
        operations.set('database', async () => {
            const trx = this.databaseParticipant.getTransaction(transactionId);

            if (!trx) {
                throw new Error('No transaction found');
            }

            // Process business logic
            await this.processMessage(message, trx);
        });

        // Execute 2PC transaction
        const success = await this.coordinator.executeTransaction(transactionId, operations);

        if (success) {
            console.log(`Message ${message.id} processed exactly once`);
        } else {
            console.log(`Message ${message.id} processing failed, will retry`);
        }

        return success;
    }

    // Process message (implement in subclass)
    protected async processMessage(message: Message, trx: DatabaseTransaction): Promise<void> {
        // Default implementation
        console.log(`Processing message: ${JSON.stringify(message)}`);
    }
}
```

**两阶段提交场景示例**：

```json
// Scenario 1: Successful commit
{
  "transaction": "tx-msg-1",
  "phase_1": {
    "queue_prepare": true,
    "database_prepare": true,
    "result": "all_vote_yes"
  },
  "phase_2": {
    "queue_commit": true,
    "database_commit": true,
    "result": "committed"
  }
}

// Scenario 2: Database prepare fails
{
  "transaction": "tx-msg-2",
  "phase_1": {
    "queue_prepare": true,
    "database_prepare": false,
    "result": "prepare_failed"
  },
  "rollback": {
    "queue_rollback": true,
    "result": "rolled_back"
  }
}
```

## 涉及概念

- `two-phase commit`
- `2PC`
- `distributed transactions`
- `queue coordination`
- `database coordination`
- `atomic commit`

## 实现提示

- 第一阶段（准备）：所有参与者投票决定是否可以提交
- 第二阶段（提交）：协调器发送最终的提交决定
- 协调器：管理跨参与者的事务生命周期
- 参与者：队列和数据库都必须支持准备和提交操作
- 故障处理：超时和失败时执行回滚

## 测试用例

### 1. 执行成功的两阶段提交

应当成功执行两阶段提交事务。

输入：

```json
{"src":"coordinator","dest":"participants","body":{"type":"execute","msg_id":1,"transaction_id":"tx-1","participants":["queue","database"]}}
```

期望输出：

```text
{"type": "committed", "in_reply_to": 1, "transaction_id": "tx-1", "phase": "commit_complete"}
```

### 2. 处理准备阶段失败

应当在准备阶段失败时执行回滚。

输入：

```json
{"src":"coordinator","dest":"participants","body":{"type":"execute","msg_id":1,"transaction_id":"tx-2","participants":["queue","database"],"database_prepare":false}}
```

期望输出：

```text
{"type": "rolled_back", "in_reply_to": 1, "transaction_id": "tx-2", "phase": "rollback_complete"}
```

## 参考资料

- [Two-Phase Commit](https://www.datastax.com/dev/blog/what-is-two-phase-commit)：两阶段提交协议详解

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
