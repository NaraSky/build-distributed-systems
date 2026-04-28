# Implement Randomized Election Timeout

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-3-election-timeout>

Track: 5. The Elector
Task order: 3
Short title: Election Timeout
Difficulty: intermediate
Subtrack: Raft Leader Election

## Problem

Add randomized election timeouts. When a follower does not hear from a leader within its timeout, it becomes a candidate. Randomization helps prevent multiple nodes from starting elections simultaneously.

## Concept Notes

### Randomized Timeouts

If all nodes used the same timeout, network hiccups could cause multiple simultaneous elections, splitting votes and delaying leader selection. Random timeouts spread out elections, usually letting one node win quickly.

## Concepts

- randomization
- timeout
- split brain prevention

## Hints

- Use random timeout between 150-300ms
- Reset timeout on heartbeat
- Different timeouts reduce split votes

## Test Cases

### 1. Random timeout in range 150-300ms

Each response contains a timeout_ms field in range 150-300. Values should vary due to randomization.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":2}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":3}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":4}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":4,"msg_id":3}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
