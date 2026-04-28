# Implement Event Replay

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-2-event-replay>

Track: 29. The Reactor
Task order: 2
Short title: Event Replay
Difficulty: intermediate
Subtrack: Event Sourcing

## Problem

Event replay rebuilds an aggregate's state by applying all of its stored events in order. It is the core read mechanism in event sourcing: state is never stored directly, only derived by replaying history.

Implement a node that supports three replay modes:

```json
// Full replay: apply all events to get current state
{ "type": "replay", "msg_id": 1, "aggregate_id": "user-123" }
-> { "type": "replayed", "in_reply_to": 1,
    "aggregate_id": "user-123",
    "events_replayed": 5, "state": {"name": "Jane"} }

// Snapshot-based replay: load snapshot, apply only events after its version
{ "type": "replay", "msg_id": 2,
  "aggregate_id": "user-123", "use_snapshot": true }
-> { "type": "replayed", "in_reply_to": 2,
    "aggregate_id": "user-123",
    "snapshot_version": 100, "events_replayed": 2 }

// Temporal query: replay only events up to the given timestamp
{ "type": "get_state", "msg_id": 3,
  "aggregate_id": "user-123", "timestamp": "2024-01-15T09:00:00Z" }
-> { "type": "state", "in_reply_to": 3,
    "aggregate_id": "user-123",
    "timestamp": "2024-01-15T09:00:00Z",
    "state": {"name": "John Doe"} }
```

For snapshot-based replay, `events_replayed` counts only events applied after the snapshot version. Temporal queries ignore any event recorded after the requested timestamp.

## Concepts

- event replay
- state reconstruction
- snapshot-based replay
- temporal query
- fold over events

## Hints

- Replay applies each event in sequence order to rebuild state from scratch
- With a snapshot, start from the saved state and only replay events after that version
- A temporal query replays only events with timestamp <= the target time
- Merge each event_data dict into the running state dict on every replay step
- snapshot_version in the response is the version at which the snapshot was taken

## Test Cases

### 1. Replay events to rebuild state

Should replay all events and return final state.

Input:

```json
{"src":"replayer","dest":"eventstore","body":{"type":"replay","msg_id":1,"aggregate_id":"user-123"}}
```

Expected output:

```text
{"type": "replayed", "in_reply_to": 1, "aggregate_id": "user-123", "events_replayed": 5, "state": {"name": "Jane"}}
```

### 2. Replay from snapshot

Should start from snapshot and replay only newer events.

Input:

```json
{"src":"replayer","dest":"eventstore","body":{"type":"replay","msg_id":1,"aggregate_id":"user-123","use_snapshot":true}}
```

Expected output:

```text
{"type": "replayed", "in_reply_to": 1, "aggregate_id": "user-123", "snapshot_version": 100, "events_replayed": 2}
```

## Resources

- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html): Martin Fowler's introduction to event sourcing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
