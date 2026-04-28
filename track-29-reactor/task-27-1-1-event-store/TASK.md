# Implement Event Store

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-1-event-store>

Track: 29. The Reactor
Task order: 1
Short title: Event Store
Difficulty: intermediate
Subtrack: Event Sourcing

## Problem

An event store is an **append-only log** where every change to an aggregate is recorded as an immutable event. To reconstruct current state you replay all events in order — or start from a snapshot. Overwriting state is never allowed.

Implement a node that manages events for multiple aggregates with **optimistic concurrency control**: the caller declares which version they expect; if another writer already changed the aggregate, the append is rejected.

```json
// Append an event (version must match current aggregate version)
{ "type": "append", "msg_id": 1,
  "aggregate_id": "user-123", "event_type": "UserCreated",
  "event_data": {"name": "John"}, "version": 0 }
-> { "type": "appended", "in_reply_to": 1,
    "event_id": "<uuid>", "sequence_number": 1 }

// Version mismatch -> reject
{ "type": "append", "version": 5 }   // actual version is 0
-> { "type": "concurrency_error", "in_reply_to": 1,
    "error": "Expected version 5, got 0" }

// Save a snapshot at the aggregate's current version
{ "type": "create_snapshot", "msg_id": 3, "aggregate_id": "user-123" }
-> { "type": "snapshot_created", "in_reply_to": 3,
    "aggregate_id": "user-123", "version": 1 }
```

Each aggregate starts at version 0. Every successful append increments its version by 1 and advances the global sequence number.

## Concepts

- event sourcing
- append-only log
- optimistic concurrency
- aggregate
- sequence number
- snapshot

## Hints

- Events are immutable — never update or delete, only append
- Track a version per aggregate; reject appends where the sent version does not match current
- Sequence numbers are global and monotonically increasing across all aggregates
- A snapshot stores the aggregate state at a specific version to speed up replay
- Return a generated event_id and the new sequence_number on success

## Test Cases

### 1. Append event to store

Should append event and return a new event_id and sequence_number=1.

Input:

```json
{"src":"service","dest":"eventstore","body":{"type":"append","msg_id":1,"aggregate_id":"user-123","event_type":"UserCreated","event_data":{"name":"John"},"version":0}}
```

Expected output:

```text
{"type": "appended", "in_reply_to": 1, "event_id": ".*", "sequence_number": 1}
```

### 2. Detect concurrent modification

Version mismatch should return a concurrency_error.

Input:

```json
{"src":"service","dest":"eventstore","body":{"type":"append","msg_id":1,"aggregate_id":"user-123","event_type":"UserUpdated","event_data":{"name":"Jane"},"version":5}}
```

Expected output:

```text
{"type": "concurrency_error", "in_reply_to": 1, "error": "Expected version 5, got 0"}
```

## Resources

- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html): Martin Fowler's introduction to event sourcing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
