# Implement Line-Delimited Framing (Redis RESP Style)

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-2-2-line-delimited>

Track: 17. The Networker
Task order: 7
Short title: Line-Delimited Framing
Difficulty: intermediate
Subtrack: Message Framing and Serialization

## Problem

Implement line-delimited framing where messages end with `\r\n`. This is the approach used by Redis RESP, HTTP/1.1 headers, and SMTP.

The challenge: TCP doesn't guarantee that a full line arrives in one read. You must buffer partial reads correctly.

Implement handlers:

```json
Request:  {"type": "line_encode", "msg_id": 1, "message": "PING"}
Response: {"type": "line_encode_ok", "in_reply_to": 1, "encoded": "PING\r\n", "bytes": 6}

Request:  {"type": "line_decode", "msg_id": 2, "buffer": "PING\r\nPONG\r\n"}
Response: {"type": "line_decode_ok", "in_reply_to": 2, "messages": ["PING", "PONG"], "remaining": ""}

Request:  {"type": "line_decode", "msg_id": 3, "buffer": "PING\r\nPON"}
Response: {"type": "line_decode_ok", "in_reply_to": 3, "messages": ["PING"], "remaining": "PON"}
```

## Concepts

- line-delimited
- RESP protocol
- CRLF
- partial reads
- buffer management

## Hints

- Messages are terminated by \r\n (CRLF)
- Buffer incoming bytes until you find a complete \r\n
- Handle the case where \r\n is split across two TCP reads
- This is similar to how Redis RESP protocol works
- Return an error for messages that exceed a maximum length limit

## Test Cases

### 1. Encode a line message

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"line_encode","msg_id":2,"message":"PING"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "line_encode_ok", "in_reply_to": 2, "encoded": "PING\r\n", "bytes": 6, "msg_id": 1}}
```

### 2. Decode multiple complete lines

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"line_decode","msg_id":2,"buffer":"GET key1\r\nSET key2 val\r\n"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "line_decode_ok", "in_reply_to": 2, "messages": ["GET key1", "SET key2 val"], "remaining": "", "msg_id": 1}}
```

## Resources

- [Redis Serialization Protocol (RESP)](https://redis.io/docs/reference/protocol-spec/): Redis protocol specification using CRLF-delimited framing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
