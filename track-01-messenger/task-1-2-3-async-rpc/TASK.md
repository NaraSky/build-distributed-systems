# Implement Async RPC Using Callbacks

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-3-async-rpc>

Track: 1. The Messenger
Task order: 8
Short title: Async RPC
Difficulty: intermediate
Subtrack: RPC and the Request-Response Model

## Problem

Synchronous RPC blocks the caller until a reply arrives, which prevents the node from handling other messages during that time. In high-throughput distributed systems, **asynchronous RPC** is preferred.

Your task is to implement an `async_rpc` method that:

1. Sends a message to a target node
2. Registers a callback function keyed by the outgoing `msg_id`
3. Returns immediately (non-blocking)
4. When a reply arrives (with matching `in_reply_to`), invokes the callback with the reply body

Implement a `batch_echo` message type: the node receives a list of strings, sends an `echo` RPC for each one to itself (loopback), and collects all replies using callbacks. Once all replies are collected, respond with the results.

```json
Request:  {"type": "batch_echo", "msg_id": 1, "values": ["a", "b", "c"]}
Response: {"type": "batch_echo_ok", "in_reply_to": 1, "results": ["a", "b", "c"]}
```

For testing, the node should echo to itself (src and dest are the same node).

## Concepts

- asynchronous programming
- callbacks
- non-blocking I/O
- event-driven

## Hints

- Store callbacks in a dictionary keyed by msg_id
- When a reply arrives, look up the callback by in_reply_to and invoke it
- The callback should receive the reply body as its argument
- Use a handler map to dispatch different message types
- Async RPC allows the node to continue processing other messages while waiting

## Test Cases

### 1. Init and echo still work

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"async"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "async", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Callback registration sends RPC

The async_rpc should send an echo message to itself. The callback fires when the reply arrives in a subsequent message.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"batch_echo","msg_id":2,"values":["x"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n1", "body": {"type": "echo", "echo": "x", "msg_id": 1}}
```

## Resources

- [Callback-Based Asynchronous Programming](https://en.wikipedia.org/wiki/Callback_(computer_programming)): Overview of callback patterns in programming

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
