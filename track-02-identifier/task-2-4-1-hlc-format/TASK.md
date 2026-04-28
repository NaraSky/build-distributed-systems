# Understand and Implement HLC Format

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-1-hlc-format>

Track: 2. The Identifier
Task order: 16
Short title: HLC Format
Difficulty: advanced
Subtrack: Hybrid Logical Clocks (HLC)

## Problem

Hybrid Logical Clocks (HLC), used in CockroachDB and Spanner, combine physical time with a logical counter. The format is `(physical_ms, logical_counter)`.

Rules for updating HLC on a **local event or send**:
1. Get current physical time `pt`
2. If `pt > hlc.pt`: set `hlc.pt = pt`, `hlc.lc = 0`
3. Else: keep `hlc.pt`, increment `hlc.lc += 1`

Implement an HLC with `hlc_tick` and `hlc_get` handlers:

```json
Request:  {"type": "hlc_tick", "msg_id": 1}
Response: {"type": "hlc_tick_ok", "in_reply_to": 1, "pt": 1234567, "lc": 0}
```

```json
Request:  {"type": "hlc_get", "msg_id": 2}
Response: {"type": "hlc_get_ok", "in_reply_to": 2, "pt": 1234567, "lc": 0}
```

## Concepts

- HLC
- hybrid clock
- physical time
- logical counter

## Hints

- HLC is a tuple: (physical_time_ms, logical_counter)
- Physical time comes from the system clock
- Logical counter disambiguates events within the same millisecond
- HLC always moves forward, even if clock goes backward
- On send: if pt > max_pt, reset counter; else increment counter

## Test Cases

### 1. HLC tick returns pt and lc

hlc_tick_ok should contain pt > 0 and lc = 0 (first tick gets fresh physical time).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. HLC get returns initial zero state

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_get","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_get_ok", "pt": 0, "lc": 0, "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Hybrid Logical Clocks (Kulkarni et al.)](https://cse.buffalo.edu/tech-reports/2014-04.pdf): Original HLC paper by Kulkarni, Demirbas, et al.

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
