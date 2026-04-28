# Implement Synchronous RPC with Timeout

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-1-sync-rpc>

Track: 1. The Messenger
Task order: 6
Short title: Sync RPC
Difficulty: intermediate
Subtrack: RPC and the Request-Response Model

## Problem

In a distributed system, nodes often need to call remote procedures on other nodes and wait for the result. This is called **synchronous RPC** (Remote Procedure Call).

Your task is to extend your Maelstrom node with a `sync_rpc` method that:

1. Sends a message to another node
2. Blocks until a response is received (matched by `in_reply_to`)
3. Returns the response body
4. Times out after a configurable duration (default: 1 second)

The node should still handle `init` and `echo` messages. Additionally, implement a `proxy` message type: when your node receives a `proxy` request, it forwards the inner message to the target node using `sync_rpc`, waits for the reply, and returns it to the original caller.

```
Request:  {"type": "proxy", "msg_id": 1, "target": "n2", "inner": {"type": "echo", "echo": "hello"}}
Response: {"type": "proxy_ok", "in_reply_to": 1, "result": {"type": "echo_ok", "echo": "hello", ...}}
```

For this task, simulate the remote node's response inline (since Maelstrom test harness sends single-node input). Your `sync_rpc` should store callbacks and resolve them when matching replies arrive.

## Concepts

- RPC
- synchronous communication
- timeout
- blocking calls

## Hints

- Use a dictionary to store pending requests keyed by msg_id
- Block the caller using threading.Event or a simple polling loop
- Set a timeout so the caller does not block forever
- When a response arrives, match it via in_reply_to and unblock the caller
- Return None or raise an exception if the timeout expires

## Test Cases

### 1. Init and echo still work

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"hello"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "hello", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Proxy sends RPC to target

The node should forward the inner message to n2 via sync_rpc. The RPC will timeout since n2 is not present, but the outgoing message to n2 must be emitted.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"proxy","msg_id":2,"target":"n2","inner":{"type":"echo","echo":"test"}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "echo", "echo": "test", "msg_id": 1}}
```

## Resources

- [Remote Procedure Calls in Distributed Systems](https://www.cs.cornell.edu/courses/cs5414/2017fa/lectures/lec-rpc.pdf): Cornell lecture on RPC semantics and failure modes

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
