# Implement Protocol Evolution

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-4-protocol-evolution>

Track: 27. The Migrator
Task order: 9
Short title: Protocol Evolution
Difficulty: advanced
Subtrack: Protocol and API Evolution

## Problem

As services evolve, they add new fields and change message schemas. Protocol evolution strategies ensure old services can still read new messages (by ignoring unknown fields) and new services can still serve old clients (by transforming messages down to old schemas).

Implement a node that handles protocol encoding, decoding, negotiation, and transformation:

```json
// Encode a message with Protocol Buffers
{ "type": "encode", "msg_id": 1, "format": "protobuf",
  "data": {"id":1,"email":"user@example.com","full_name":"John Doe"} }
-> { "type": "encoded", "in_reply_to": 1,
    "format": "protobuf", "encoded": "<base64>",
    "fields": ["id","email","full_name"] }

// Old schema decodes v2 message: unknown fields are silently dropped
{ "type": "decode", "msg_id": 2, "format": "protobuf",
  "schema": "v1", "data": "<base64-v2>" }
-> { "type": "decoded", "in_reply_to": 2,
    "schema": "v1",
    "data": {"id":1,"email":"user@example.com"},
    "unknown_fields_ignored": true }

// Negotiate highest common version
{ "type": "negotiate", "msg_id": 3,
  "client_versions": ["1.0","2.0"] }
-> { "type": "negotiated", "in_reply_to": 3,
    "version": "2.0",
    "server_versions": ["1.0","2.0","3.0"] }
```

## Concepts

- Protocol Buffers
- backward compatibility
- unknown field handling
- version negotiation
- message transformation

## Hints

- Protocol Buffers: unknown fields from a newer schema are ignored by older readers
- Decode with old schema: ignore fields the old schema does not know about
- Protocol negotiation: choose the highest version that both client and server support
- Transform v2->v1: map new field names back to old names (full_name -> name)
- Encoding returns the field names actually serialised into the message

## Test Cases

### 1. Protocol Buffers backward compatibility

Should encode all three fields and return base64 representation.

Input:

```json
{"src":"client_v1","dest":"service","body":{"type":"encode","msg_id":1,"format":"protobuf","data":{"id":1,"email":"user@example.com","full_name":"John Doe"}}}
```

Expected output:

```text
{"type": "encoded", "in_reply_to": 1, "format": "protobuf", "encoded": ".*", "fields": ["id", "email", "full_name"]}
```

### 2. Decode with old schema (ignores unknown fields)

Old v1 schema should decode v2 message and silently drop full_name.

Input:

```json
{"src":"service","dest":"decoder","body":{"type":"decode","msg_id":1,"format":"protobuf","schema":"v1","data":"BASE64_ENCODED_V2"}}
```

Expected output:

```text
{"type": "decoded", "in_reply_to": 1, "schema": "v1", "data": {"id": 1, "email": "user@example.com"}, "unknown_fields_ignored": true}
```

## Resources

- [Protocol Buffers](https://protobuf.dev/): Protocol Buffers: language-neutral, extensible serialization format
- [API Protocol Evolution](https://www.connolly.tech/p/api-protocol-evolution/): API Protocol Evolution guide

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
