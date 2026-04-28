# Implement Command Side Validation and Execution

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-2-command-side>

Track: 29. The Reactor
Task order: 7
Short title: Command Side
Difficulty: intermediate
Subtrack: CQRS (Command Query Responsibility Segregation)

## Problem

The command side is the write path in CQRS. Before any state change is applied, the command must pass two layers of validation: **schema validation** (correct fields and types) and **business rule validation** (domain constraints). Only then is the command executed and a domain event emitted.

Implement a node that processes commands through both validation layers:

```json
// Schema error: missing required field
{ "type": "CreateUser", "msg_id": 1,
  "payload": {"name": "John"} }      // email missing
-> { "type": "validation_failed", "in_reply_to": 1,
    "valid": false, "errors": ["Email is required"] }

// Business rule error: age constraint
{ "type": "CreateUser", "msg_id": 2,
  "payload": {"name": "John", "email": "j@example.com", "age": 16} }
-> { "type": "validation_failed", "in_reply_to": 2,
    "valid": false, "errors": ["User must be 18 or older"] }

// All validation passes: execute and emit domain event
{ "type": "CreateUser", "msg_id": 3,
  "payload": {"name": "John", "email": "j@example.com", "age": 25} }
-> { "type": "command_executed", "in_reply_to": 3,
    "success": true,
    "events": [{"type": "UserCreated", "payload": {"id": "<uuid>"}}] }
```

When multiple validations fail, collect all errors and return them together. Never execute the command if any validation fails.

## Concepts

- command validation
- business rules
- command handler
- domain events
- invariant enforcement

## Hints

- Schema validation: check required fields and types before business rules
- Business rule validation: enforce domain constraints (age >= 18, unique email, etc.)
- Return all validation errors together, not just the first one
- Only call the command handler after all validation passes
- Emit a domain event (UserCreated) that describes what happened, not what was requested

## Test Cases

### 1. Validate command format

Missing email should fail schema validation.

Input:

```json
{"src":"client","dest":"commandside","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John"}}}
```

Expected output:

```text
{"type": "validation_failed", "in_reply_to": 1, "valid": false, "errors": ["Email is required"]}
```

### 2. Validate business rules

Age under 18 should fail business rule validation.

Input:

```json
{"src":"client","dest":"commandside","body":{"type":"CreateUser","msg_id":1,"payload":{"name":"John","email":"john@example.com","age":16}}}
```

Expected output:

```text
{"type": "validation_failed", "in_reply_to": 1, "valid": false, "errors": ["User must be 18 or older"]}
```

## Resources

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html): CQRS and the command side design

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
