# Handle Client Request Routing

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-2-client-routing>

Track: 7. The Store
Task order: 2
Short title: Client Routing
Difficulty: intermediate
Subtrack: Linearizable Key-Value Store

## Problem

Route client requests to the leader:

1. Client sends request to any node
2. If node is leader, process request
3. If not leader, return redirect with leader hint
4. Client follows redirect

Handle the case when leader is unknown (election in progress).

## Concept Notes

### Client Routing

Only the Raft leader can process writes. Clients must find the leader. Options: redirect to leader, proxy through leader, or use client library that tracks leader.

### Leader Discovery

Nodes learn the leader from AppendEntries. When redirecting, include the current known leader. Clients may need to retry if leader changes during the request.

## Concepts

- leader routing
- redirect
- client sessions

## Hints

- Only leader can process writes
- Redirect clients to leader
- Track leader ID

## Test Cases

### 1. Leader processes request

Leader processes read request locally without redirecting

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"become_leader","msg_id":2,"term":1}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"become_leader_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":null}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
