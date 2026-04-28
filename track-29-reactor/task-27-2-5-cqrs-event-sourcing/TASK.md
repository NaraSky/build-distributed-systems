# Implement CQRS with Event Sourcing

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-5-cqrs-event-sourcing>

Track: 29. The Reactor
Task order: 10
Short title: CQRS + Event Sourcing
Difficulty: advanced
Subtrack: CQRS (Command Query Responsibility Segregation)

## Problem

CQRS and event sourcing are designed to work together: commands write to the event store (the source of truth), and projections built from those events serve queries. This gives you the full audit trail of event sourcing plus the read performance of CQRS.

Implement a node that integrates both patterns end-to-end:

```json
// Command: validate, apply to aggregate, persist event, update projections
{ "type": "command", "msg_id": 1,
  "command": {"type": "CreateUser",
               "payload": {"id": "user-123", "name": "John"}} }
-> { "type": "command_result", "in_reply_to": 1,
    "success": true,
    "events": [{"eventType": "UserCreated", "aggregateId": "user-123"}] }

// Query: read from projection (never from event store)
{ "type": "query", "msg_id": 2,
  "query": {"type": "GetUser", "params": {"userId": "user-123"}} }
-> { "type": "query_result", "in_reply_to": 2,
    "data": {"id": "user-123", "name": "John"} }

// Temporal query: replay event store up to a point in time
{ "type": "query", "msg_id": 3,
  "query": {"type": "GetUserAtTime",
             "params": {"userId": "user-123",
                        "timestamp": "2024-01-15T09:00:00Z"}} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": {"id": "user-123", "name": "John Doe",
             "at_time": "2024-01-15T09:00:00Z"} }
```

The flow for a command is: validate -> apply to aggregate -> append event to store -> update projections. The flow for a query is: read from projection (for current state) or replay event store (for past state).

## Concepts

- CQRS
- event sourcing
- aggregate
- projection
- temporal query
- full-stack integration

## Hints

- Commands go through validation, then are applied to the aggregate, which emits events
- Events are stored in the event store and then applied to projections
- Queries read from projections, not from the event store directly
- Temporal queries replay the event store up to a given timestamp
- The aggregate version must match the expected version on every command (optimistic locking)

## Test Cases

### 1. Execute command with event sourcing

Command should emit a UserCreated event with the correct aggregateId.

Input:

```json
{"src":"client","dest":"cqrs","body":{"type":"command","msg_id":1,"command":{"type":"CreateUser","payload":{"id":"user-123","name":"John"}}}}
```

Expected output:

```text
{"type": "command_result", "in_reply_to": 1, "success": true, "events": [{"eventType": "UserCreated", "aggregateId": "user-123"}]}
```

### 2. Query from projection

Query should read from the projection, not the event store.

Input:

```json
{"src":"client","dest":"cqrs","body":{"type":"query","msg_id":1,"query":{"type":"GetUser","params":{"userId":"user-123"}}}}
```

Expected output:

```text
{"type": "query_result", "in_reply_to": 1, "data": {"id": "user-123", "name": "John"}}
```

## Resources

- [CQRS and Event Sourcing](https://martinfowler.com/bliki/CQRS.html): Combining CQRS with event sourcing for full auditability and read performance

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
