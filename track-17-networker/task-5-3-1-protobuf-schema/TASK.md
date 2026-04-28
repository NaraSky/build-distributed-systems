# Define and Encode Protocol Buffer Messages

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-1-protobuf-schema>

Track: 17. The Networker
Task order: 11
Short title: Protobuf Schema
Difficulty: intermediate
Subtrack: gRPC and Protocol Buffers

## Problem

Protocol Buffers use a schema definition (.proto file) and a compact binary wire format. Each field has a number, type, and wire encoding.

Wire format: each field is `(field_number << 3 | wire_type)` followed by the value.

Implement a protobuf encoder/decoder for a simple message:

```proto
message Person {
    string name = 1;
    int32 age = 2;
    string email = 3;
}
```

Implement handlers:

```json
Request:  {"type": "proto_define", "msg_id": 1, "schema": {"name": "Person", "fields": [
    {"name": "name", "number": 1, "type": "string"},
    {"name": "age", "number": 2, "type": "int32"},
    {"name": "email", "number": 3, "type": "string"}
]}}
Response: {"type": "proto_define_ok", "in_reply_to": 1, "message_name": "Person", "field_count": 3}

Request:  {"type": "proto_encode", "msg_id": 2, "message": "Person", "data": {"name": "Alice", "age": 30, "email": "alice@example.com"}}
Response: {"type": "proto_encode_ok", "in_reply_to": 2, "encoded_hex": "...", "size_bytes": 28}
```

## Concepts

- Protocol Buffers
- schema definition
- field numbering
- varint encoding

## Hints

- Protobuf uses field numbers instead of field names on the wire
- Varint encoding uses 7 bits per byte with MSB continuation flag
- Wire types: 0=varint, 1=64-bit, 2=length-delimited, 5=32-bit
- Each field is encoded as (field_number << 3 | wire_type)
- String fields use wire type 2: tag + length + bytes

## Test Cases

### 1. Define a protobuf schema

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"proto_define","msg_id":2,"schema":{"name":"Person","fields":[{"name":"name","number":1,"type":"string"},{"name":"age","number":2,"type":"int32"}]}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "proto_define_ok", "in_reply_to": 2, "message_name": "Person", "field_count": 2, "msg_id": 1}}
```

### 2. Encode a protobuf message

proto_encode_ok should contain valid protobuf hex encoding. Name field: tag 0x0a then length then ASCII. Age field: tag 0x10 then varint 30.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"proto_define","msg_id":2,"schema":{"name":"Person","fields":[{"name":"name","number":1,"type":"string"},{"name":"age","number":2,"type":"int32"}]}}}
{"src":"c1","dest":"n1","body":{"type":"proto_encode","msg_id":3,"message":"Person","data":{"name":"Alice","age":30}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Protocol Buffers Encoding](https://protobuf.dev/programming-guides/encoding/): How Protocol Buffers encode data on the wire (varint, length-delimited, etc.)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
