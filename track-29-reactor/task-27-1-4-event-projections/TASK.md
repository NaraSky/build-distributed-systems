# Implement Event Projections

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-4-event-projections>

Track: 29. The Reactor
Task order: 4
Short title: Event Projections
Difficulty: intermediate
Subtrack: Event Sourcing

## Problem

The event store is optimized for writes, not queries. A **projection** solves this: it listens to the event stream and maintains a denormalized read model that is fast to query. When the event schema changes or a new view is needed, the projection can be rebuilt from scratch.

Implement a node that manages named projections:

```json
// Create a new projection with an initial empty state
{ "type": "create", "msg_id": 1,
  "name": "user-listing", "initial_state": [] }
-> { "type": "projection_created", "in_reply_to": 1,
    "name": "user-listing", "version": 0 }

// Apply one event to a projection
{ "type": "update", "msg_id": 2,
  "projection": "user-listing",
  "event": {"event_type": "UserCreated",
             "event_data": {"id": "user-123", "name": "John"}} }
-> { "type": "projection_updated", "in_reply_to": 2,
    "projection": "user-listing", "version": 1,
    "state": [{"id": "user-123", "name": "John"}] }

// Rebuild projection from scratch using a list of past events
{ "type": "rebuild", "msg_id": 3,
  "projection": "user-listing",
  "events": [{"event_type": "UserCreated", "event_data": {"id": "user-123"}}] }
-> { "type": "projection_rebuilt", "in_reply_to": 3,
    "projection": "user-listing",
    "events_processed": 1, "version": 1 }
```

The projection version increments by 1 for every event applied. Rebuilding resets the version to 0 and replays all supplied events.

## Concepts

- projections
- read models
- event-driven denormalization
- rebuild
- versioned projection

## Hints

- A projection is a named read model built by consuming events one at a time
- create initializes a projection with an empty state and version 0
- update applies one event to the projection and increments its version
- rebuild replays a list of events from scratch onto the projection
- Each update/rebuild step should merge event_data into the projection state

## Test Cases

### 1. Create listing projection

Should create new projection at version 0.

Input:

```json
{"src":"projector","dest":"projection","body":{"type":"create","msg_id":1,"name":"user-listing","initial_state":[]}}
```

Expected output:

```text
{"type": "projection_created", "in_reply_to": 1, "name": "user-listing", "version": 0}
```

### 2. Update projection with event

Should append user to listing and increment version to 1.

Input:

```json
{"src":"eventstore","dest":"projection","body":{"type":"update","msg_id":1,"projection":"user-listing","event":{"event_type":"UserCreated","event_data":{"id":"user-123","name":"John"}}}}
```

Expected output:

```text
{"type": "projection_updated", "in_reply_to": 1, "projection": "user-listing", "version": 1, "state": [{"id": "user-123", "name": "John"}]}
```

## Resources

- [Projections in Event Sourcing](https://eventstore.com/blog/projections/): How projections turn events into query-optimized read models

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
