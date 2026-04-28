# Implement Event Compensation and Sagas

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-5-event-compensation>

Track: 29. The Reactor
Task order: 5
Short title: Sagas
Difficulty: advanced
Subtrack: Event Sourcing

## Problem

Distributed transactions across multiple services cannot use a single database commit. A **saga** breaks the operation into a sequence of local steps, each with a corresponding compensation action. If any step fails, all already-completed steps are rolled back by executing their compensations in reverse order.

Implement a node that executes sagas and handles failures:

```json
// Execute all steps successfully
{ "type": "execute", "msg_id": 1,
  "saga_id": "booking-123",
  "steps": ["book_flight", "book_hotel", "book_car"] }
-> { "type": "saga_completed", "in_reply_to": 1,
    "saga_id": "booking-123",
    "state": "completed", "completed_steps": 3 }

// Fail at book_hotel, compensate completed steps in reverse
{ "type": "execute", "msg_id": 2,
  "saga_id": "booking-124",
  "steps": ["book_flight", "book_hotel"],
  "fail_step": "book_hotel" }
-> { "type": "saga_compensated", "in_reply_to": 2,
    "saga_id": "booking-124",
    "state": "compensated",
    "compensated_steps": ["book_flight"] }
```

When a step fails, only the steps that were successfully completed before it need to be compensated — the failing step itself is not compensated because it never completed. Compensation order is the reverse of execution order.

## Concepts

- saga pattern
- distributed transactions
- compensation
- rollback
- choreography

## Hints

- Execute steps in order; on any failure, compensate all previously completed steps in reverse order
- fail_step in the test input tells you which step should fail — simulate that failure
- compensated_steps must list only the steps that were successfully executed before the failure
- The compensation order is reverse of execution: last completed step is compensated first
- saga_id must be echoed back in every response so the caller can correlate requests

## Test Cases

### 1. Execute saga successfully

All three steps succeed, completed_steps=3.

Input:

```json
{"src":"orchestrator","dest":"saga","body":{"type":"execute","msg_id":1,"saga_id":"booking-123","steps":["book_flight","book_hotel","book_car"]}}
```

Expected output:

```text
{"type": "saga_completed", "in_reply_to": 1, "saga_id": "booking-123", "state": "completed", "completed_steps": 3}
```

### 2. Compensate on failure

book_hotel fails, only book_flight (already completed) is compensated.

Input:

```json
{"src":"orchestrator","dest":"saga","body":{"type":"execute","msg_id":1,"saga_id":"booking-124","steps":["book_flight","book_hotel"],"fail_step":"book_hotel"}}
```

Expected output:

```text
{"type": "saga_compensated", "in_reply_to": 1, "saga_id": "booking-124", "state": "compensated", "compensated_steps": ["book_flight"]}
```

## Resources

- [Saga Pattern](https://microservices.io/patterns/data/saga.html): Chris Richardson's overview of the saga pattern for distributed transactions

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
