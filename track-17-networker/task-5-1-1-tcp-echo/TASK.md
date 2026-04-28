# Build a TCP Echo Server from Raw Syscalls

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-1-tcp-echo>

Track: 17. The Networker
Task order: 1
Short title: TCP Echo Server
Difficulty: intermediate
Subtrack: TCP From Scratch

## Problem

Build a TCP echo server using raw syscalls. No standard library network abstractions allowed. The server should:

1. Create a socket using `socket(AF_INET, SOCK_STREAM, 0)`
2. Bind to a port using `bind()`
3. Listen for connections using `listen()`
4. Accept connections using `accept()`
5. Read data using `read()`
6. Write data back using `write()`

Implement a Maelstrom node that simulates this:

```json
Request:  {"type": "tcp_echo_start", "msg_id": 1, "port": 8080}
Response: {"type": "tcp_echo_start_ok", "in_reply_to": 1, "status": "listening", "port": 8080}

Request:  {"type": "tcp_echo_send", "msg_id": 2, "data": "hello world"}
Response: {"type": "tcp_echo_send_ok", "in_reply_to": 2, "echoed": "hello world", "bytes": 11}

Request:  {"type": "tcp_echo_stats", "msg_id": 3}
Response: {"type": "tcp_echo_stats_ok", "in_reply_to": 3, "total_connections": 1, "total_bytes": 11}
```

## Concepts

- TCP
- socket
- bind
- listen
- accept
- syscalls

## Hints

- Use raw socket syscalls: socket(), bind(), listen(), accept(), read(), write()
- Do not use high-level network abstractions from the standard library
- The echo server reads data from a client and writes it back unchanged
- Use SOCK_STREAM for TCP and AF_INET for IPv4
- Close client connections properly after echoing

## Test Cases

### 1. Start echo server

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tcp_echo_start","msg_id":2,"port":8080}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_echo_start_ok", "in_reply_to": 2, "status": "listening", "port": 8080, "msg_id": 1}}
```

### 2. Echo data back correctly

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tcp_echo_start","msg_id":2,"port":8080}}
{"src":"c1","dest":"n1","body":{"type":"tcp_echo_send","msg_id":3,"data":"hello world"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_echo_start_ok", "in_reply_to": 2, "status": "listening", "port": 8080, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_echo_send_ok", "in_reply_to": 3, "echoed": "hello world", "bytes": 11, "msg_id": 2}}
```

## Resources

- [Beej Guide to Network Programming](https://beej.us/guide/bgnet/): Classic guide to Unix socket programming from raw syscalls

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
