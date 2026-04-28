# Implement Echo Service with Proper Acknowledgment

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-echo-service>

Track: 1. The Messenger
Task order: 3
Short title: Echo Service
Difficulty: beginner
Subtrack: Hello, Distributed World

## Problem

The echo workload is the simplest Maelstrom workload. Clients send echo messages containing a value, and your node must echo that value back.

Request format:

```json
{
  "type": "echo",
  "msg_id": 1,
  "echo": "Please echo 35"
}
```

Expected response:

```json
{
  "type": "echo_ok",
  "msg_id": 1,
  "in_reply_to": 1,
  "echo": "Please echo 35"
}
```

Combine your init handling from the previous task with a new echo handler. Your node should handle both message types.

## Concept Notes

## Remote Procedure Calls (RPC)

Echo is the simplest form of **RPC**: a client sends a request and expects a response. While trivial, this pattern forms the basis of all distributed communication.

### The Request-Response Pattern

Complex systems like Raft are built from many request-response interactions:

```text
Client                          Server
  |                               |
  |------- Request (echo) ------->|
  |                               |
  |<------ Response (echo_ok) ----|
  |                               |
```

### Handler Dispatch

Your node needs to **dispatch messages** to appropriate handlers based on type. This is a pattern you will use throughout:

  - Examine the message `type` field

  - Route to the correct handler function

  - Generate and send the appropriate response

### Pseudocode

```text
for each message from stdin:
    parse JSON
    switch message.body.type:
        case "init":
            store node_id and node_ids
            reply with init_ok
        case "echo":
            reply with echo_ok containing the echo value
        default:
            log unknown message type
```

### Idempotency

Echo is naturally **idempotent** - calling it multiple times with the same input produces the same output. This property is valuable in distributed systems where messages may be retried.

## Concepts

- RPC
- request-response
- message handling

## Hints

- Echo messages contain an "echo" field with the value to echo back
- Response type is "echo_ok"
- Include the original echo value in your response

## Test Cases

### 1. Echo response

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"hello"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "hello", "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Echo Workload](https://fly.io/dist-sys/1/): Fly.io Gossip Glomers Echo challenge walkthrough

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
