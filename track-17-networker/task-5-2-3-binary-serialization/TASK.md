# Implement a Binary Serialization Format

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-3-binary-serialization>

Track: 17. The Networker
Task order: 8
Short title: Binary Serialization
Difficulty: advanced
Subtrack: Message Framing and Serialization

## Problem

Implement a binary serialization format (similar to MessagePack). Support four types: integers, strings, arrays, and maps. Compare size and performance to JSON.

Type tags:
- `0x01`: integer (4 bytes big-endian)
- `0x02`: string (2-byte length + UTF-8 bytes)
- `0x03`: array (2-byte count + N encoded values)
- `0x04`: map (2-byte count + N key-value pairs)

Implement handlers:

```json
Request:  {"type": "bin_encode", "msg_id": 1, "value": {"name": "Alice", "age": 30}}
Response: {"type": "bin_encode_ok", "in_reply_to": 1, "encoded_hex": "...", "size_bytes": 20, "json_size_bytes": 27, "savings_pct": 25.9}

Request:  {"type": "bin_decode", "msg_id": 2, "encoded_hex": "..."}
Response: {"type": "bin_decode_ok", "in_reply_to": 2, "value": {"name": "Alice", "age": 30}}

Request:  {"type": "bin_benchmark", "msg_id": 3, "payload_sizes": [100, 1000, 10000]}
Response: {"type": "bin_benchmark_ok", "in_reply_to": 3, "results": [
    {"size": 100, "json_bytes": 100, "binary_bytes": 72, "ratio": 0.72}
]}
```

## Concepts

- binary serialization
- MessagePack
- type tags
- compact encoding

## Hints

- Use a type tag byte before each value: 0x01=int, 0x02=string, 0x03=array, 0x04=map
- Integers use a fixed 4-byte big-endian encoding
- Strings are prefixed with a 2-byte length followed by UTF-8 bytes
- Arrays are prefixed with a 2-byte count, followed by that many encoded values
- Compare the encoded size to JSON for the same data

## Test Cases

### 1. Encode a simple integer

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bin_encode","msg_id":2,"value":42}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bin_encode_ok", "in_reply_to": 2, "encoded_hex": "010000002a", "size_bytes": 5, "msg_id": 1}}
```

### 2. Encode and decode roundtrip

Encode should produce hex for string "hello". Decode of that hex should return "hello".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bin_encode","msg_id":2,"value":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"bin_decode","msg_id":3,"encoded_hex":"02000568656c6c6f"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [MessagePack Specification](https://msgpack.org/): MessagePack: an efficient binary serialization format

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
