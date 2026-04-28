# Implement CQRS Fundamentals

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-1-cqrs-fundamentals>

Track: 29. The Reactor
Task order: 6
Short title: CQRS Fundamentals
Difficulty: intermediate
Subtrack: CQRS (Command Query Responsibility Segregation)

## Problem

CQRS (Command Query Responsibility Segregation) separates every operation into either a **command** (write, changes state) or a **query** (read, never changes state). Commands and queries are handled by separate buses with separate models, enabling each side to be optimised independently.

Implement a node that routes messages to the correct bus:

```json
// Command: validate payload, apply change, return emitted events
{ "type": "CreateUser", "msg_id": 1,
  "payload": {"name": "John", "email": "john@example.com"} }
-> { "type": "command_result", "in_reply_to": 1,
    "success": true,
    "events": [{"type": "UserCreated", "payload": {"id": "<uuid>", "name": "John"}}] }

// Command validation failure
{ "type": "CreateUser", "msg_id": 2,
  "payload": {"name": "John"} }    // missing email
-> { "type": "command_result", "in_reply_to": 2,
    "success": false,
    "errors": ["Email is required"] }

// Query: read from read model, no state change
{ "type": "GetUser", "msg_id": 3,
  "params": {"user_id": "user-123"} }
-> { "type": "query_result", "in_reply_to": 3,
    "data": {"id": "user-123", "name": "John Doe"} }
```

The key rule: if the operation changes state, it is a command; if it only reads, it is a query. A single operation must never do both.

## Concepts

- CQRS
- command bus
- query bus
- command validation
- read model
- write model separation

## Hints

- Commands change state and emit events; queries only read and never mutate
- A command handler validates the payload, applies the change, and returns the emitted events
- A query handler reads from a pre-built read model and returns data
- Validation failure should return success=false with an errors array
- Route by the message type field: CreateUser goes to command bus, GetUser to query bus

## Test Cases

### 1. Handle command

Valid command should succeed and return emitted events.

Input:

```json
{"src":"client","dest":"commandbus","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John","email":"john@example.com"}}}
```

Expected output:

```text
{"type": "command_result", "in_reply_to": 1, "success": true, "events": [{"type": "UserCreated", "payload": {"id": ".*", "name": "John"}}]}
```

### 2. Execute query

Query should return data from read model without changing state.

Input:

```json
{"src":"client","dest":"querybus","body":{"type":"GetUser","msg_id":1,"params":{"user_id":"user-123"}}}
```

Expected output:

```text
{"type": "query_result", "in_reply_to": 1, "data": {"id": "user-123", "name": "John Doe"}}
```

## Resources

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html): Martin Fowler's explanation of Command Query Responsibility Segregation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
