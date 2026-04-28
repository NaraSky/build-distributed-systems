# Implement HLC Receive Rule

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-2-hlc-receive>

Track: 2. The Identifier
Task order: 17
Short title: HLC Receive
Difficulty: advanced
Subtrack: Hybrid Logical Clocks (HLC)

## Problem

The HLC receive rule is more complex than Lamport's. On receiving a message with HLC `(msg.pt, msg.lc)`:

1. `new_pt = max(local.pt, msg.pt, now_ms())`
2. If `new_pt == local.pt == msg.pt`: `new_lc = max(local.lc, msg.lc) + 1`
3. Elif `new_pt == local.pt`: `new_lc = local.lc + 1`
4. Elif `new_pt == msg.pt`: `new_lc = msg.lc + 1`
5. Else (new physical time): `new_lc = 0`

Implement a `hlc_receive` handler:
```json
Request:  {"type": "hlc_receive", "msg_id": 1, "remote_pt": 1000, "remote_lc": 5}
Response: {"type": "hlc_receive_ok", "in_reply_to": 1, "pt": 1000, "lc": 6}
```

## Concepts

- HLC merge
- receive rule
- clock synchronization
- causal consistency

## Hints

- On receive: take max of local pt, received pt, and current physical time
- If the max pt equals local pt and received pt, increment lc from max of both lc values
- If max pt equals only one side, take that sides lc and increment
- If max pt is the new physical time, reset lc to 0
- HLC must always advance - never go backward

## Test Cases

### 1. Receive from ahead remote advances local

Remote pt is far future. new_pt=remote_pt, new_lc=remote_lc+1=6.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"n2","dest":"n1","body":{"type":"hlc_receive","msg_id":2,"remote_pt":9999999999999,"remote_lc":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "hlc_receive_ok", "pt": 9999999999999, "lc": 6, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Receive from behind remote uses local

After tick, local pt is current time. Remote pt=0 is behind. new_pt=max(local,0,now). lc depends on whether now advanced.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"hlc_receive","msg_id":3,"remote_pt":0,"remote_lc":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [CockroachDB and HLC](https://www.cockroachlabs.com/blog/living-without-atomic-clocks/): How CockroachDB uses HLC for transaction ordering

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
