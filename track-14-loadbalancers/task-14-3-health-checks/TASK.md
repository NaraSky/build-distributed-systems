# Add Health Checks and Failover

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-3-health-checks>

Track: 14. Load Balancers
Task order: 3
Short title: Health Checks
Difficulty: intermediate
Subtrack: Layer 4 Load Balancing

## Problem

Add health checking to your load balancer:

1. Periodically send health check requests to servers
2. Track consecutive failures per server
3. Mark server unhealthy after N failures
4. Exclude unhealthy servers from selection
5. Re-add servers after successful health checks

Support both active (probing) and passive (observing failures) checks.

## Concept Notes

### Health Checking

Health checks detect server failures before routing requests to them. Active checks send periodic probes (HTTP GET /health). Passive checks observe real request failures.

### Graceful Degradation

When servers fail, the load balancer redistributes traffic to healthy servers. Slow re-introduction (ramping up traffic) prevents overwhelming recovering servers.

## Concepts

- health check
- failover
- liveness

## Hints

- Periodically probe each server
- Mark unhealthy after consecutive failures
- Remove from rotation until healthy

## Test Cases

### 1. Exclude unhealthy server

Input:

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"c1","dest":"lb","body":{"type":"health_status","msg_id":2,"server":"s1","consecutive_failures":5,"threshold":3}}
{"src":"c2","dest":"lb","body":{"type":"get_healthy_servers","msg_id":3}}
```

Expected output:

```text
{"src":"lb","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"lb","dest":"c1","body":{"type":"health_status_ok","in_reply_to":2,"msg_id":1,"status":"unhealthy"}}
{"src":"lb","dest":"c2","body":{"type":"get_healthy_servers_ok","in_reply_to":3,"msg_id":2,"healthy":["s2","s3"]}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
