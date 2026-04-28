# Implement Exponential Backoff for Retries

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-5-exponential-backoff>

Track: 1. The Messenger
Task order: 10
Short title: Exponential Backoff
Difficulty: intermediate
Subtrack: RPC and the Request-Response Model

## Problem

Fixed-interval retries can overwhelm a recovering system. When many nodes retry at the same interval, they create a **thundering herd** that prevents recovery. **Exponential backoff** spreads retries over time.

Your task is to implement `rpc_with_backoff` that:

1. On the first attempt, waits `base_delay` (default: 100ms) before retrying
2. On each subsequent attempt, doubles the delay: `delay = base_delay * 2^attempt`
3. Adds random jitter: `delay += random(0, delay * 0.1)` to decorrelate retries
4. Caps the total delay at `max_delay` (default: 2 seconds)
5. Gives up after `max_retries` attempts (default: 5)

Implement a `backoff_relay` message type:

```json
Request:  {"type": "backoff_relay", "msg_id": 1, "target": "n2", "payload": {"type": "read"}}
Response: {"type": "backoff_relay_ok", "in_reply_to": 1, "attempts": 3, "total_delay_ms": 700}
```

The response includes the number of attempts and total delay in milliseconds. For this task, focus on the backoff calculation logic. Your node should output the computed delay schedule.

Write a comment in your code explaining why exponential backoff helps under high load (at least 100 words).

## Concepts

- exponential backoff
- jitter
- congestion control
- load management

## Hints

- Base delay doubles with each attempt: delay = base_delay * 2^attempt
- Add random jitter to prevent thundering herd: delay += random(0, delay * 0.5)
- Cap the maximum delay to prevent unreasonably long waits
- Log each retry with the computed delay for observability
- The total wait time is the sum of all delays, not just the last one

## Test Cases

### 1. Init and echo still work

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"backoff"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "backoff", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Compute backoff returns schedule

The node should respond with a compute_backoff_ok containing schedule_ms array, total_ms, and retries. Due to jitter the exact values vary, but the response structure must be correct.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compute_backoff","msg_id":2,"max_retries":3,"base_delay":0.1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/): AWS Architecture Blog on backoff strategies with detailed analysis
- [TCP Congestion Control](https://en.wikipedia.org/wiki/TCP_congestion_control): How TCP uses exponential backoff for congestion avoidance

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
