# Add Heartbeat Mechanism

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-2-heartbeat>

Track: 5. The Elector
Task order: 2
Short title: Heartbeat
Difficulty: intermediate
Subtrack: Raft Leader Election

## Problem

Implement heartbeats from the leader to followers. The leader periodically sends AppendEntries (empty for now) to maintain authority. Followers that do not receive heartbeats become candidates.

## Concept Notes

### Heartbeats

Heartbeats serve dual purposes: they prevent followers from starting elections, and they carry log replication data (in full Raft). A leader that stops sending heartbeats will be replaced.

## Concepts

- heartbeat
- liveness
- failure detection

## Hints

- Leader sends heartbeats periodically
- Followers reset timeout on heartbeat
- Missing heartbeats trigger election

## Test Cases

### 1. Leader sends heartbeat

Leader sends heartbeat append_entries to all peers (n2, n3).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"become_leader","msg_id":2,"term":1}}
{"src":"c0","dest":"n1","body":{"type":"wait","msg_id":3,"duration_ms":150}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"become_leader_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"n2","body":{"type":"append_entries","msg_id":2,"term":1,"leader_id":"n1","prev_log_index":0,"prev_log_term":0,"entries":[],"leader_commit":0}}
{"src":"n1","dest":"n3","body":{"type":"append_entries","msg_id":3,"term":1,"leader_id":"n1","prev_log_index":0,"prev_log_term":0,"entries":[],"leader_commit":0}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
