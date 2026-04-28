# Implement Least Connections Algorithm

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-2-least-connections>

Track: 14. Load Balancers
Task order: 2
Short title: Least Connections
Difficulty: intermediate
Subtrack: Layer 4 Load Balancing

## Problem

Implement least-connections load balancing:

1. Track active connection count for each server
2. When a request starts, increment count for chosen server
3. When a request completes, decrement count
4. Route new requests to server with fewest connections

This adapts to varying request durations automatically.

## Concept Notes

### Least Connections

Round robin fails when requests have varying durations - slow requests can pile up on one server. Least connections routes to the server with fewest active requests, naturally balancing load.

### Weighted Least Connections

Combine weights with connection counts: select server with lowest (connections / weight) ratio. This accounts for both current load and server capacity.

## Concepts

- least connections
- dynamic load
- connection tracking

## Hints

- Track active connections per server
- Increment on request, decrement on complete
- Select server with fewest connections

## Test Cases

### 1. Balance by connections

Load balancer with 3 backends: s1 (2 active connections), s2 (5 connections), s3 (1 connection). New request arrives. Verify it routes to s3 (fewest connections). After request completes, connection count decreases.

Input:

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"c1","dest":"lb","body":{"type":"set_connections","msg_id":2,"server":"s1","count":2}}
{"src":"c2","dest":"lb","body":{"type":"set_connections","msg_id":3,"server":"s2","count":5}}
{"src":"c3","dest":"lb","body":{"type":"set_connections","msg_id":4,"server":"s3","count":1}}
{"src":"c4","dest":"lb","body":{"type":"route_request","msg_id":5}}
```

Expected output:

```text
{"src": "lb", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "lb", "dest": "c1", "body": {"type": "set_connections_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "lb", "dest": "c2", "body": {"type": "set_connections_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "lb", "dest": "c3", "body": {"type": "set_connections_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "lb", "dest": "c4", "body": {"type": "route_request_ok", "server": "s1", "in_reply_to": 5, "msg_id": 4}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
