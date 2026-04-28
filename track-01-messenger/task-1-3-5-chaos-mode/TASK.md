# Add Chaos Mode with Random Message Dropping

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-5-chaos-mode>

Track: 1. The Messenger
Task order: 15
Short title: Chaos Mode
Difficulty: intermediate
Subtrack: The Protocol Beneath

## Problem

Real networks drop messages. Netflix pioneered **chaos engineering** — deliberately injecting failures to test resilience. Your task is to add a "chaos mode" to your node.

When chaos mode is enabled, the node randomly drops a configurable percentage of **outgoing** messages (does not send them to stdout). This simulates network packet loss.

Implement these message types:

1. `chaos_on` — Enable chaos mode with a given drop rate:
```json
Request:  {"type": "chaos_on", "msg_id": 1, "drop_rate": 0.1}
Response: {"type": "chaos_on_ok", "in_reply_to": 1, "drop_rate": 0.1}
```

2. `chaos_off` — Disable chaos mode:
```json
Request:  {"type": "chaos_off", "msg_id": 2}
Response: {"type": "chaos_off_ok", "in_reply_to": 2}
```

3. `chaos_stats` — Report chaos statistics:
```json
Request:  {"type": "chaos_stats", "msg_id": 3}
Response: {"type": "chaos_stats_ok", "in_reply_to": 3, "enabled": true, "drop_rate": 0.1, "total_sent": 50, "total_dropped": 5}
```

Use a fixed random seed (42) for reproducibility in tests. The drop decision uses `random.random() < drop_rate`.

Chaos mode should NOT drop control messages (`init_ok`, `chaos_on_ok`, `chaos_off_ok`, `chaos_stats_ok`) — only application messages like `echo_ok`.

## Concepts

- chaos engineering
- fault injection
- resilience testing
- network partitions

## Hints

- Use a random number generator to decide whether to drop each outgoing message
- The drop rate should be configurable (default 10%)
- Log dropped messages to stderr so you can observe chaos effects
- Track how many messages were dropped vs sent
- Chaos mode should be toggleable via a message

## Test Cases

### 1. Init and echo work without chaos

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"safe"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "safe", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Chaos on responds with drop_rate

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chaos_on","msg_id":2,"drop_rate":0.5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "chaos_on_ok", "drop_rate": 0.5, "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Principles of Chaos Engineering](https://principlesofchaos.org/): The foundational document on chaos engineering methodology
- [Netflix Chaos Monkey](https://netflix.github.io/chaosmonkey/): Netflix tool for randomly terminating instances in production

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
