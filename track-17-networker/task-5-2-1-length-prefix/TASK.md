# Implement Length-Prefixed Message Framing

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-1-length-prefix>

Track: 17. The Networker
Task order: 6
Short title: Length-Prefix Framing
Difficulty: intermediate
Subtrack: Message Framing and Serialization

## Problem

TCP is a byte stream, not a message protocol. You need framing to know where one message ends and the next begins. Length-prefixed framing prepends each message with its size.

Format: `[4-byte big-endian length][payload]`

Implement `send_frame` and `recv_frame`:

```json
Request:  {"type": "frame_encode", "msg_id": 1, "payload": "hello world"}
Response: {"type": "frame_encode_ok", "in_reply_to": 1, "frame_hex": "0000000b68656c6c6f20776f726c64", "total_bytes": 15}

Request:  {"type": "frame_decode", "msg_id": 2, "frame_hex": "0000000b68656c6c6f20776f726c64"}
Response: {"type": "frame_decode_ok", "in_reply_to": 2, "payload": "hello world", "payload_length": 11}

Request:  {"type": "frame_decode_partial", "msg_id": 3, "chunks": ["0000000b68", "656c6c6f20", "776f726c64"]}
Response: {"type": "frame_decode_partial_ok", "in_reply_to": 3, "payload": "hello world", "chunks_needed": 3}
```

## Concepts

- message framing
- length prefix
- TCP stream
- partial reads

## Hints

- Each message is [4-byte big-endian length][payload]
- The receiver must read exactly 4 bytes first to get the length
- Then read exactly length bytes for the payload
- TCP does not guarantee message boundaries; handle partial reads
- Use a buffer to accumulate bytes until a full frame is available

## Test Cases

### 1. Encode a simple message

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"frame_encode","msg_id":2,"payload":"hello"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "frame_encode_ok", "in_reply_to": 2, "frame_hex": "0000000568656c6c6f", "total_bytes": 9, "msg_id": 1}}
```

### 2. Decode a framed message

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"frame_decode","msg_id":2,"frame_hex":"0000000568656c6c6f"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "frame_decode_ok", "in_reply_to": 2, "payload": "hello", "payload_length": 5, "msg_id": 1}}
```

## Resources

- [Message Framing in TCP](https://blog.stephencleary.com/2009/04/message-framing.html): Comprehensive overview of different message framing strategies for TCP

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
