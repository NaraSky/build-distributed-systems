# Model Message Format with Typed Schema

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-1-typed-schema>

Track: 1. The Messenger
Task order: 11
Short title: Typed Schema
Difficulty: intermediate
Subtrack: The Protocol Beneath

## Problem

Raw JSON is just strings. A typed schema wraps the raw message in classes with explicit fields, validation, and serialization methods — making it impossible to accidentally send a malformed message.

Implement a `Message` class with `to_json()` / `from_json()` methods and a `MessageBody` class. Your node handles `init`, `echo`, and a new `validate` message type:

```json
{ "type": "validate", "msg_id": 1,
  "payload": "{\"src\":\"a\",\"dest\":\"b\",\"body\":{\"type\":\"x\"}}" }
-> { "type": "validate_ok", "in_reply_to": 1,
    "valid": true, "fields": ["src", "dest", "body.type"] }
```

The `validate` handler parses the JSON string in `payload` and reports which top-level and nested fields are present. If the payload is not valid JSON, return `valid: false` with an empty `fields` list.

## Concepts

- serialization
- deserialization
- schema design
- type safety

## Hints

- Define a Message class with src, dest, and body fields
- Body should have type, msg_id, and in_reply_to fields at minimum
- Implement to_json() and from_json() methods for serialization
- Validate field types during deserialization
- Handle missing optional fields with sensible defaults

## Test Cases

### 1. Init and echo with typed schema

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"typed"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "typed", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Validate a well-formed payload

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"validate","msg_id":2,"payload":"{\"src\":\"a\",\"dest\":\"b\",\"body\":{\"type\":\"x\"}}"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "validate_ok", "valid": true, "fields": ["src", "dest", "body.type"], "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Protocol Buffers Overview](https://protobuf.dev/overview/): How Google defines typed message schemas for distributed systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
