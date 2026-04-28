# Implement a Lamport Clock

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-1-lamport-clock>

Track: 2. The Identifier
Task order: 11
Short title: Lamport Clock
Difficulty: intermediate
Subtrack: Logical Clocks as IDs

## Problem

Leslie Lamport showed that in a distributed system, you don't need physical clocks to order events. A **Lamport clock** is a simple counter that provides a partial order: if event A causally precedes event B, then L(A) < L(B).

Rules:
1. Before any **send**, increment then stamp the message
2. On **receive**, set counter = max(local_counter, message_counter) + 1
3. On any **local event**, increment the counter

Your task is to implement a Lamport clock in your Maelstrom node:

```json
Request:  {"type": "tick", "msg_id": 1}
Response: {"type": "tick_ok", "in_reply_to": 1, "clock": 1}
```

The `tick` handler triggers a local event (increment). Also handle `send_stamped` which sends a message with the current Lamport timestamp to another node:

```json
Request:  {"type": "send_stamped", "msg_id": 1, "target": "n2", "data": "hello"}
Response: {"type": "send_stamped_ok", "in_reply_to": 1, "clock": 2}
```

And a `get_clock` handler that returns the current clock value:
```json
Response: {"type": "get_clock_ok", "in_reply_to": 1, "clock": 5}
```

## Concepts

- Lamport clock
- logical time
- partial order
- happens-before

## Hints

- A Lamport clock is a single integer counter per node
- On every local event or send: increment the counter
- On receive: counter = max(local, received) + 1
- Lamport clocks give a partial order, not a total order
- If L(A) < L(B), it does NOT mean A happened before B

## Test Cases

### 1. Tick increments clock

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "clock": 1, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Multiple ticks increment sequentially

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "clock": 1, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "clock": 2, "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "clock": 3, "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [Time, Clocks, and the Ordering of Events (Lamport 1978)](https://lamport.azurewebsites.net/pubs/time-clocks.pdf): The original paper by Leslie Lamport on logical clocks

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
