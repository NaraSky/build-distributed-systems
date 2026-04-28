# 实现 Two-Phase Commit用于队列和Database

英文标题：Implement Two-Phase Commit用于Queue和Database
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-5-two-phase-commit>

课程：15. 队列
任务序号：10
短标题：Two-Phase Commit
难度：advanced
子主题：Exactly-Once Delivery

## 中文导读

本题要求你完成 `实现 Two-Phase Commit用于队列和Database`。

重点关注：`two-phase commit`、`2PC`、`distributed transactions`、`queue coordination`、`database coordination`。

建议先按提示逐步实现：Phase 1: Prepare - both participants vote to commit。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Two-phase commit (2PC) coordinates atomic commits across multiple 分布式系统, ensuring all participants commit or rollback together.

**Problem**: Coordinate commits across 队列和database. Scenario: 1) Consumer receives 消息, 2) Consumer updates database, 3) Consumer commits database, 4) Consumer crashes before ACK, 5) 队列 re-delivers 消息, 6) Database already updated (duplicate!). Solution: Two-phase commit.

**Phase 1 - Prepare**: 队列 prepares to ACK 消息, Database prepares to commit 事务, Both vote YES or NO.

**Phase 2 - Commit/Rollback**: If both vote YES: Commit both, If any votes NO: Rollback both.

**Benefits**: Atomic commit across systems, No partial updates, Exactly-once semantics, 故障-tolerant coordination.

**Two-phase commit coordinator**:

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

    // Execute distributed 事务
    async executeTransaction(
        transactionId: string,
        operations: Map<string, () => Promise<void>>
    ): Promise<boolean> {
        // Initialize 事务 state
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
        console.日志(`事务 ${transactionId}: Prepare phase`);

        const state = this.transactions.get(transactionId)!;
        state.status = 'preparing';

        // Prepare all participants
       用于(const [participantId, participant] of this.participants) {
            try {
                console.日志(`Preparing participant ${participantId}`);

                // Execute prepare operation
                const operation = operations.get(participantId);

                if (operation) {
                    await operation();
                }

                // Ask participant to prepare
                const vote = await participant.prepare(transactionId);

                state.votes.set(participantId, vote);

                if (!vote) {
                    console.日志(`Participant ${participantId} voted NO`);
                    state.status = 'prepare_failed';
                    return false;
                }

                console.日志(`Participant ${participantId} voted YES`);

            } catch (error) {
                console.error(`Participant ${participantId} prepare failed:`, error);
                state.votes.set(participantId, false);
                state.status = 'prepare_failed';
                return false;
            }
        }

        state.status = 'prepared';
        console.日志(`事务 ${transactionId}: All participants voted YES`);
        return true;
    }

    // Phase 2: Commit
    private async commitPhase(transactionId: string): Promise<void> {
        console.日志(`事务 ${transactionId}: Commit phase`);

        const state = this.transactions.get(transactionId)!;
        state.status = 'committing';

        // Commit all participants
       用于(const [participantId, participant] of this.participants) {
            try {
                console.日志(`Committing participant ${participantId}`);
                await participant.commit(transactionId);
                console.日志(`Participant ${participantId} committed`);
            } catch (error) {
                console.error(`Participant ${participantId} commit failed:`, error);
                // Note: In real 2PC, commit failures require recovery
            }
        }

        state.status = 'committed';
        console.日志(`事务 ${transactionId}: Committed`);

        // Cleanup
        this.transactions.delete(transactionId);
    }

    // Rollback phase
    private async rollbackPhase(transactionId: string): Promise<void> {
        console.日志(`事务 ${transactionId}: Rollback phase`);

        const state = this.transactions.get(transactionId)!;
        state.status = 'rolling_back';

        // Rollback all participants
       用于(const [participantId, participant] of this.participants) {
            try {
                // Only rollback participants that voted YES
                if (state.votes.get(participantId) === true) {
                    console.日志(`Rolling back participant ${participantId}`);
                    await participant.rollback(transactionId);
                    console.日志(`Participant ${participantId} rolled back`);
                }
            } catch (error) {
                console.error(`Participant ${participantId} rollback failed:`, error);
            }
        }

        state.status = 'rolled_back';
        console.日志(`事务 ${transactionId}: Rolled back`);

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

**队列 participant**:

```typescript
class QueueParticipant implements Participant {
    id = '队列';
    private 队列: MessageQueue;
    private preparedMessages: Map<string, 消息> = new Map();

    constructor(队列: MessageQueue) {
        this.队列 = 队列;
    }

    // Prepare to ACK 消息
    async prepare(transactionId: string): Promise<boolean> {
        console.日志(`队列: Prepare用于事务 ${transactionId}`);

        try {
            // Check if 消息 exists和can be ACKed
            const 消息 = this.preparedMessages.get(transactionId);

            if (!消息) {
                console.日志(`队列: No 消息用于事务 ${transactionId}`);
                return false;
            }

            // Reserve 消息 (don't ACK yet)
            console.日志(`队列: 消息 reserved用于事务 ${transactionId}`);
            return true;

        } catch (error) {
            console.error(`队列: Prepare failed用于事务 ${transactionId}:`, error);
            return false;
        }
    }

    // Commit ACK
    async commit(transactionId: string): Promise<void> {
        console.日志(`队列: Commit用于事务 ${transactionId}`);

        const 消息 = this.preparedMessages.get(transactionId);

        if (消息) {
            // ACK the 消息
            await this.队列.ack(消息.id, 消息.offset);
            console.日志(`队列: 消息 ${消息.id} ACKed`);
            this.preparedMessages.delete(transactionId);
        }
    }

    // Rollback (release reservation)
    async rollback(transactionId: string): Promise<void> {
        console.日志(`队列: Rollback用于事务 ${transactionId}`);

        // Release 消息 (will be re-delivered)
        this.preparedMessages.delete(transactionId);
        console.日志(`队列: 消息 released用于事务 ${transactionId}`);
    }

    // Prepare 消息用于事务
    prepareMessage(transactionId: string, 消息: 消息): void {
        this.preparedMessages.set(transactionId, 消息);
        console.日志(`队列: 消息 prepared用于事务 ${transactionId}`);
    }
}
```

**Database participant**:

```typescript
class DatabaseParticipant implements Participant {
    id = 'database';
    private database: Database;
    private transactions: Map<string, DatabaseTransaction> = new Map();

    constructor(database: Database) {
        this.database = database;
    }

    // Prepare 事务
    async prepare(transactionId: string): Promise<boolean> {
        console.日志(`Database: Prepare用于事务 ${transactionId}`);

        try {
            // Start 事务
            const trx = await this.database.beginTransaction();

            // Store 事务用于later commit/rollback
            this.transactions.set(transactionId, trx);

            console.日志(`Database: 事务 prepared用于${transactionId}`);
            return true;

        } catch (error) {
            console.error(`Database: Prepare failed用于事务 ${transactionId}:`, error);
            return false;
        }
    }

    // Commit 事务
    async commit(transactionId: string): Promise<void> {
        console.日志(`Database: Commit用于事务 ${transactionId}`);

        const trx = this.transactions.get(transactionId);

        if (trx) {
            await trx.commit();
            this.transactions.delete(transactionId);
            console.日志(`Database: 事务 ${transactionId} committed`);
        }
    }

    // Rollback 事务
    async rollback(transactionId: string): Promise<void> {
        console.日志(`Database: Rollback用于事务 ${transactionId}`);

        const trx = this.transactions.get(transactionId);

        if (trx) {
            await trx.rollback();
            this.transactions.delete(transactionId);
            console.日志(`Database: 事务 ${transactionId} rolled back`);
        }
    }

    // Get 事务用于operations
    getTransaction(transactionId: string): DatabaseTransaction | undefined {
        return this.transactions.get(transactionId);
    }
}
```

**Exactly-once consumer，包含2PC**:

```typescript
class ExactlyOnceConsumerWith2PC {
    private coordinator: TwoPhaseCommitCoordinator;
    private queueParticipant: QueueParticipant;
    private databaseParticipant: DatabaseParticipant;

    constructor(队列: MessageQueue, database: Database) {
        this.coordinator = new TwoPhaseCommitCoordinator();
        this.queueParticipant = new QueueParticipant(队列);
        this.databaseParticipant = new DatabaseParticipant(database);

        // Register participants
        this.coordinator.registerParticipant(this.queueParticipant);
        this.coordinator.registerParticipant(this.databaseParticipant);
    }

    // Consume 消息，包含exactly-once semantics
    async consume(消息: 消息): Promise<boolean> {
        const transactionId = `tx-${消息.id}`;
        console.日志(`Processing 消息 ${消息.id}，包含2PC`);

        // Prepare 队列 participant
        this.queueParticipant.prepareMessage(transactionId, 消息);

        // Define 事务 operations
        const operations = new Map<string, () => Promise<void>>();

        // Database operation
        operations.set('database', async () => {
            const trx = this.databaseParticipant.getTransaction(transactionId);

            if (!trx) {
                throw new Error('No 事务 found');
            }

            // Process business logic
            await this.processMessage(消息, trx);
        });

        // Execute 2PC 事务
        const success = await this.coordinator.executeTransaction(transactionId, operations);

        if (success) {
            console.日志(`消息 ${消息.id} processed exactly once`);
        } else {
            console.日志(`消息 ${消息.id} processing failed, will 重试`);
        }

        return success;
    }

    // Process 消息 (implement in subclass)
    protected async processMessage(消息: 消息, trx: DatabaseTransaction): Promise<void> {
        // Default implementation
        console.日志(`Processing 消息: ${JSON.stringify(消息)}`);
    }
}
```

**Example 2PC scenarios**:

```JSON
// Scenario 1: Successful commit
{
  "事务": "tx-msg-1",
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
  "事务": "tx-msg-2",
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

- Phase 1: Prepare - both participants vote to commit
- Phase 2: Commit - coordinator sends final commit decision
- Coordinator: Manages the 事务 across participants
- Participants: 队列和database must support prepare/commit
- 故障 handling: 超时和rollback on failures

## 测试用例

### 1. Execute successful 2PC

Should execute successful 2PC 事务.

输入：

```json
{"src":"coordinator","dest":"participants","body":{"type":"execute","msg_id":1,"transaction_id":"tx-1","participants":["queue","database"]}}
```

期望输出：

```text
{"type": "committed", "in_reply_to": 1, "transaction_id": "tx-1", "phase": "commit_complete"}
```

### 2.处理prepare failure

Should rollback on prepare 故障.

输入：

```json
{"src":"coordinator","dest":"participants","body":{"type":"execute","msg_id":1,"transaction_id":"tx-2","participants":["queue","database"],"database_prepare":false}}
```

期望输出：

```text
{"type": "rolled_back", "in_reply_to": 1, "transaction_id": "tx-2", "phase": "rollback_complete"}
```

## 参考资料

- [Two-Phase Commit](https://www.datastax.com/dev/blog/what-is-two-phase-commit)：Two-phase commit protocol

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
