# Implement Event Versioning and Migration

Website: <https://builddistributedsystem.com/tracks/reactor/tasks/task-27-1-3-event-versioning>

Track: 29. The Reactor
Task order: 3
Short title: Event Versioning
Difficulty: advanced
Subtrack: Event Sourcing

## Problem

Event schemas change over time as requirements evolve. A field gets added, renamed, or split. Because old events are immutable, you cannot change them in place — instead you **upcast** them: transform older versions to the current schema on read.

Implement a node that handles event schema migration through upcasting:

```json
// Upcast a single event from v1 to v2
// v1 UserCreated has: id, name
// v2 UserCreated adds: email (default "")
{ "type": "upcast", "msg_id": 1,
  "event": {"event_type": "UserCreated", "version": 1,
            "event_data": {"id": 1, "name": "John"}},
  "target_version": 2 }
-> { "type": "upcasted", "in_reply_to": 1,
    "event": {"event_type": "UserCreated", "version": 2,
              "event_data": {"id": 1, "name": "John", "email": ""}} }

// Migrate a batch of events to the target version
{ "type": "migrate_batch", "msg_id": 2,
  "events": [
    {"event_type": "UserCreated", "version": 1, "event_data": {"id": 1}}
  ],
  "target_version": 2 }
-> { "type": "migrated", "in_reply_to": 2,
    "count": 1, "target_version": 2 }
```

Your upcaster must handle multi-step migration (e.g. v1 -> v2 -> v3) by chaining single-version upgrades. Each step adds or defaults the fields introduced in that version.

## Concepts

- event versioning
- schema evolution
- upcasting
- backward compatibility
- migration

## Hints

- Upcasting transforms an old event version to the target version in-place
- When upcasting from v1 to v2, fill missing fields with sensible defaults (empty string, 0, etc.)
- migrate_batch iterates over the events array and upcasts each one
- count in the migrate_batch response is the total number of events processed
- Events already at the target version should be returned unchanged

## Test Cases

### 1. Upcast event to new version

Should add missing email field with default empty string when upcasting v1->v2.

Input:

```json
{"src":"migrator","dest":"eventstore","body":{"type":"upcast","msg_id":1,"event":{"event_type":"UserCreated","version":1,"event_data":{"id":1,"name":"John"}},"target_version":2}}
```

Expected output:

```text
{"type": "upcasted", "in_reply_to": 1, "event": {"event_type": "UserCreated", "version": 2, "event_data": {"id": 1, "name": "John", "email": ""}}}
```

### 2. Migrate batch of events

Should migrate all events and return count.

Input:

```json
{"src":"migrator","dest":"eventstore","body":{"type":"migrate_batch","msg_id":1,"events":[{"event_type":"UserCreated","version":1,"event_data":{"id":1}}],"target_version":2}}
```

Expected output:

```text
{"type": "migrated", "in_reply_to": 1, "count": 1, "target_version": 2}
```

## Resources

- [Event Versioning Patterns](https://leanpub.com/esversioning/read): Greg Young's guide to versioning events in event-sourced systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
