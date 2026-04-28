# Implement Two-Phase Commit for Queue and Database

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-29-2-5-two-phase-commit>

Track: 15. Queues
Task order: 10
Short title: Two-Phase Commit
Difficulty: advanced
Subtrack: Exactly-Once Delivery

## Problem

Two-phase commit (2PC) coordinates atomic commits across multiple distributed systems, ensuring all participants commit or rollback together.

**Problem**: Coordinate commits across queue and database. Scenario: 1) Consumer receives message, 2) Consumer updates database, 3) Consumer commits database, 4) Consumer crashes before ACK, 5) Queue re-delivers message, 6) Database already updated (duplicate!). Solution: Two-phase commit.

**Phase 1 - Prepare**: Queue prepares to ACK message, Database prepares to commit transaction, Both vote YES or NO.

**Phase 2 - Commit/Rollback**: If both vote YES: Commit both, If any votes NO: Rollback both.

**Benefits**: Atomic commit across systems, No partial updates, Exactly-once semantics, Fault-tolerant coordination.

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

**Queue participant**:

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

**Database participant**:

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

**Exactly-once consumer with 2PC**:

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

**Example 2PC scenarios**:

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

## Concepts

- two-phase commit
- 2PC
- distributed transactions
- queue coordination
- database coordination
- atomic commit

## Hints

- Phase 1: Prepare - both participants vote to commit
- Phase 2: Commit - coordinator sends final commit decision
- Coordinator: Manages the transaction across participants
- Participants: Queue and database must support prepare/commit
- Failure handling: Timeout and rollback on failures

## Test Cases

### 1. Execute successful 2PC

Should execute successful 2PC transaction.

Input:

```json
{"src":"coordinator","dest":"participants","body":{"type":"execute","msg_id":1,"transaction_id":"tx-1","participants":["queue","database"]}}
```

Expected output:

```text
{"type": "committed", "in_reply_to": 1, "transaction_id": "tx-1", "phase": "commit_complete"}
```

### 2. Handle prepare failure

Should rollback on prepare failure.

Input:

```json
{"src":"coordinator","dest":"participants","body":{"type":"execute","msg_id":1,"transaction_id":"tx-2","participants":["queue","database"],"database_prepare":false}}
```

Expected output:

```text
{"type": "rolled_back", "in_reply_to": 1, "transaction_id": "tx-2", "phase": "rollback_complete"}
```

## Resources

- [Two-Phase Commit](https://www.datastax.com/dev/blog/what-is-two-phase-commit): Two-phase commit protocol

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
