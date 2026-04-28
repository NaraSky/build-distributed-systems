# Implement Event-Driven Read Model Updates

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-2-4-event-driven-updates>

Track: 29. The Reactor
Task order: 9
Short title: Event-Driven Updates
Difficulty: intermediate
Subtrack: CQRS (Command Query Responsibility Segregation)

## Problem

In CQRS, the command side emits events and the query side must react to those events to keep its read models up-to-date. An **event-driven projector** subscribes to the event bus and updates one or more read models whenever a relevant event arrives.

Implement a node that acts as a projector with subscription and idempotent update support:

```json
// Register interest in specific event types
{ "type": "subscribe", "msg_id": 1,
  "event_types": ["UserCreated", "UserUpdated"] }
-> { "type": "subscribed", "in_reply_to": 1,
    "event_types": ["UserCreated", "UserUpdated"] }

// Event arrives: update all relevant read models
{ "type": "event", "msg_id": 2,
  "event": {"type": "UserCreated",
             "payload": {"id": "user-123", "name": "John"}} }
-> { "type": "read_models_updated", "in_reply_to": 2,
    "event_id": "evt-123",
    "updated_models": ["user_listing", "user_by_email"] }

// Same event_id arrives again: skip it
{ "type": "event", "msg_id": 3,
  "event": {"type": "UserCreated", "id": "evt-123",
             "payload": {"id": "user-123"}} }
-> { "type": "event_skipped", "in_reply_to": 3,
    "event_id": "evt-123", "reason": "already_processed" }
```

Idempotency is critical: the event bus may deliver the same event more than once. Always check the event_id before applying any update.

## Concepts

- event bus
- projector
- subscription
- idempotent updates
- eventual consistency

## Hints

- subscribe registers the projector to receive the listed event types from the event bus
- When an event arrives, update every read model that cares about that event type
- Track processed event IDs; return event_skipped for duplicates (idempotency)
- updated_models lists the names of all read models that were actually updated
- Eventual consistency: read models may lag slightly behind the write model

## Test Cases

### 1. Subscribe to events

Should acknowledge subscription to both event types.

Input:

```json
{"src":"projector","dest":"eventbus","body":{"type":"subscribe","msg_id":1,"event_types":["UserCreated","UserUpdated"]}}
```

Expected output:

```text
{"type": "subscribed", "in_reply_to": 1, "event_types": ["UserCreated", "UserUpdated"]}
```

### 2. Update read models on event

UserCreated should update both user_listing and user_by_email read models.

Input:

```json
{"src":"eventbus","dest":"projector","body":{"type":"event","msg_id":1,"event":{"type":"UserCreated","payload":{"id":"user-123","name":"John"}}}}
```

Expected output:

```text
{"type": "read_models_updated", "in_reply_to": 1, "event_id": "evt-123", "updated_models": ["user_listing", "user_by_email"]}
```

## Resources

- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html): Event-driven read model updates in CQRS

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
