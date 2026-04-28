# Implement Protocol Versioning with Backward Compatibility

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-5-protocol-versioning>

Track: 17. The Networker
Task order: 10
Short title: Protocol Versioning
Difficulty: intermediate
Subtrack: Message Framing and Serialization

## Problem

Implement a protocol versioning scheme. The sender includes a `protocol_version` in the header. The receiver handles backward compatibility for older versions.

Protocol versions:
- **v1**: `{version: 1, key: string, value: string}`
- **v2**: `{version: 2, key: string, value: string|int, timestamp_ms: number, tags: string[]}`

When receiving a v1 message, upgrade it to v2 with defaults: `timestamp_ms = 0`, `tags = []`.

Implement handlers:

```json
Request:  {"type": "proto_send_v1", "msg_id": 1, "key": "name", "value": "Alice"}
Response: {"type": "proto_send_v1_ok", "in_reply_to": 1, "wire_version": 1}

Request:  {"type": "proto_send_v2", "msg_id": 2, "key": "age", "value": 30, "timestamp_ms": 1700000000, "tags": ["user"]}
Response: {"type": "proto_send_v2_ok", "in_reply_to": 2, "wire_version": 2}

Request:  {"type": "proto_receive", "msg_id": 3, "wire_version": 1, "key": "name", "value": "Alice"}
Response: {"type": "proto_receive_ok", "in_reply_to": 3, "parsed_version": 2, "key": "name", "value": "Alice", "timestamp_ms": 0, "tags": []}
```

## Concepts

- protocol versioning
- backward compatibility
- wire format
- migration

## Hints

- Include a protocol_version field in the message header
- Version 1: basic key-value with string values only
- Version 2: adds integer values and a timestamp field
- The receiver must handle both v1 and v2 messages
- Use sensible defaults for missing fields when upgrading v1 to v2

## Test Cases

### 1. Send v1 message

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"proto_send_v1","msg_id":2,"key":"name","value":"Alice"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "proto_send_v1_ok", "in_reply_to": 2, "wire_version": 1, "msg_id": 1}}
```

### 2. Receive v1 message upgraded to v2

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"proto_receive","msg_id":2,"wire_version":1,"key":"name","value":"Alice"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "proto_receive_ok", "in_reply_to": 2, "parsed_version": 2, "key": "name", "value": "Alice", "timestamp_ms": 0, "tags": [], "msg_id": 1}}
```

## Resources

- [Protocol Buffers - Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/): How Protocol Buffers handle schema evolution and backward compatibility

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
