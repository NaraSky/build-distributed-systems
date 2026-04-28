# Pass the Maelstrom G-Counter Workload

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-5-maelstrom-counter>

Track: 4. The Counter
Task order: 10
Short title: Maelstrom Counter
Difficulty: advanced
Subtrack: G-Counter and PN-Counter

## Problem

The Maelstrom g-counter workload is the definitive correctness test for your CRDT counter implementation. It runs your nodes in a simulated distributed environment and verifies that the counter behaves correctly under concurrent operations.

**Workload operations**:
- `add`: increment the counter by a delta value
- `read`: return the current counter value

**Checker properties**:
1. Every read value must be <= the sum of all add operations (no over-counting)
2. The counter must be eventually consistent (all nodes converge to the same value)
3. The counter must be monotonically non-decreasing per node (G-Counter property)

**Running the test**:
```
maelstrom test -w g-counter --bin your_node --node-count 3 --rate 100 --time-limit 20
```

```json
Request:  {"type": "add", "msg_id": 1, "delta": 5}
Response: {"type": "add_ok", "in_reply_to": 1}

Request:  {"type": "read", "msg_id": 2}
Response: {"type": "read_ok", "in_reply_to": 2, "value": 42}
```

## Concepts

- Maelstrom
- g-counter workload
- correctness verification
- linearizability check
- distributed testing

## Hints

- The Maelstrom g-counter workload sends add and read operations to your nodes
- Your implementation must handle: init, add (delta), read
- Nodes must gossip state to ensure eventual consistency across the cluster
- The checker verifies: reads never exceed the sum of all adds
- Use the PN-Counter implementation from the previous task as the foundation

## Test Cases

### 1. Add and read operations

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":5}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 3, "value": 5, "msg_id": 2}}
```

### 2. Read never exceeds total adds

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":10}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":3,"delta":20}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 4, "value": 30, "msg_id": 3}}
```

## Resources

- [Maelstrom G-Counter](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-g-counter): Maelstrom documentation on the g-counter workload

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
