# Implement Timeout and Retry Loop for RPC

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-2-timeout-retry>

Track: 1. The Messenger
Task order: 7
Short title: Timeout & Retry
Difficulty: intermediate
Subtrack: RPC and the Request-Response Model

## Problem

In distributed systems, messages can be lost or delayed indefinitely. A single RPC call with a timeout is not enough — you need a **retry loop** to handle transient failures.

Your task is to implement a `rpc_with_retry` method that:

1. Sends an RPC to the target node
2. Waits for a reply with a timeout (default: 500ms)
3. If no reply arrives, retries the RPC (with a new msg_id)
4. Gives up after `max_retries` attempts (default: 3)
5. Returns the response body on success, or None after all retries fail

Implement a `relay` message type to test this: when your node receives a `relay` request, it uses `rpc_with_retry` to forward a message to the target node.

```json
Request:  {"type": "relay", "msg_id": 1, "target": "n2", "payload": {"type": "read"}}
Response: {"type": "relay_ok", "in_reply_to": 1, "attempts": 3, "result": {...}}
```

The response should include the number of attempts made. If all retries fail, respond with an error:
```json
{"type": "error", "in_reply_to": 1, "code": 0, "text": "RPC failed after 3 attempts"}
```

## Concepts

- timeout
- retry logic
- fault tolerance
- at-least-once delivery

## Hints

- Wrap your sync_rpc in a loop that retries on timeout
- Track the number of attempts and give up after max_retries
- Each retry should use a new msg_id for the outgoing message
- Log each retry attempt to stderr for observability
- Return the first successful response or an error after exhausting retries

## Test Cases

### 1. Init and echo still work with retry node

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"retry-test"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "retry-test", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Relay emits outgoing RPC message

First retry attempt sends the RPC to n2. Subsequent retries may also emit messages but the test only checks first output.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"relay","msg_id":2,"target":"n2","payload":{"type":"read"}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "read", "msg_id": 1}}
```

## Resources

- [Retry Patterns in Distributed Systems](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/): AWS Builders Library on timeout and retry strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
