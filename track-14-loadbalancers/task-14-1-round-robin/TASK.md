# Implement Round Robin Load Balancer

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-1-round-robin>

Track: 14. Load Balancers
Task order: 1
Short title: Round Robin
Difficulty: beginner
Subtrack: Layer 4 Load Balancing

## Problem

Implement round robin load balancing:

1. Maintain an ordered list of backend servers
2. Track current server index
3. For each request, send to server at current index
4. Increment index (wrapping to 0 at end)

Round robin distributes load evenly when requests have similar cost.

## Concept Notes

### Round Robin

Round robin is the simplest load balancing algorithm. Requests cycle through servers in order: 1, 2, 3, 1, 2, 3... It works well when servers are identical and requests have similar processing cost.

### Weighted Round Robin

When servers have different capacities, weighted round robin sends proportionally more requests to stronger servers. A server with weight 3 gets three turns for every one turn of a weight-1 server.

## Concepts

- round robin
- load balancing
- stateless

## Hints

- Track current position in server list
- Increment and wrap on each request
- Handle empty server list

## Test Cases

### 1. Even distribution

Load balancer with 3 backends (s1, s2, s3). Send 6 requests. Verify round-robin distributes evenly: req1->s1, req2->s2, req3->s3, req4->s1, req5->s2, req6->s3. Each backend gets exactly 2 requests.

Input:

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"c1","dest":"lb","body":{"type":"add_servers","msg_id":2,"servers":["s1","s2","s3"]}}
{"src":"c2","dest":"lb","body":{"type":"get_server","msg_id":3}}
{"src":"c3","dest":"lb","body":{"type":"get_server","msg_id":4}}
{"src":"c4","dest":"lb","body":{"type":"get_server","msg_id":5}}
```

Expected output:

```text
{"src": "lb", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "lb", "dest": "c1", "body": {"type": "add_servers_ok", "servers": ["s1", "s2", "s3"], "in_reply_to": 2, "msg_id": 1}}
{"src": "lb", "dest": "c2", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 3, "msg_id": 2}}
{"src": "lb", "dest": "c3", "body": {"type": "get_server_ok", "server": "s2", "in_reply_to": 4, "msg_id": 3}}
{"src": "lb", "dest": "c4", "body": {"type": "get_server_ok", "server": "s3", "in_reply_to": 5, "msg_id": 4}}
```

### 2. Wrap around

Load balancer with 2 backends (s1, s2). Send 5 requests. Verify counter wraps: req1->s1, req2->s2, req3->s1 (wrap), req4->s2, req5->s1. Index should reset to 0 after reaching end of server list.

Input:

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2"]}}
{"src":"c1","dest":"lb","body":{"type":"add_servers","msg_id":2,"servers":["s1","s2"]}}
{"src":"c2","dest":"lb","body":{"type":"get_server","msg_id":3}}
{"src":"c3","dest":"lb","body":{"type":"get_server","msg_id":4}}
{"src":"c4","dest":"lb","body":{"type":"get_server","msg_id":5}}
```

Expected output:

```text
{"src": "lb", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "lb", "dest": "c1", "body": {"type": "add_servers_ok", "servers": ["s1", "s2"], "in_reply_to": 2, "msg_id": 1}}
{"src": "lb", "dest": "c2", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 3, "msg_id": 2}}
{"src": "lb", "dest": "c3", "body": {"type": "get_server_ok", "server": "s2", "in_reply_to": 4, "msg_id": 3}}
{"src": "lb", "dest": "c4", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 5, "msg_id": 4}}
```

## Resources

- [Load Balancing Algorithms](https://www.nginx.com/blog/choosing-nginx-plus-load-balancing-techniques/): NGINX guide to load balancing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
