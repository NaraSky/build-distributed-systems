# Implement Traffic Splitting in Service Mesh

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-3-traffic-splitting>

Track: 28. The Orchestrator
Task order: 8
Short title: Traffic Splitting
Difficulty: intermediate
Subtrack: Service Mesh

## Problem

Traffic splitting lets you roll out a new version gradually instead of switching all users at once. You can send a small percentage to the new version (canary), route specific users by request headers (A/B test), or split 50/50 (blue-green).

Implement a node that routes requests according to splitting rules:

```json
// Weighted split: 80% to v1, 20% to v2
{ "type": "route", "msg_id": 1 }
{ traffic_split: {"v1": 80, "v2": 20} }
-> { "type": "routed", "in_reply_to": 1,
    "version": "v1", "reason": "weighted_routing" }

// Header-based routing overrides weight
{ "type": "route", "msg_id": 2,
  "headers": {"x-beta": "true"} }
-> { "type": "routed", "in_reply_to": 2,
    "version": "v2", "reason": "header_match" }

// Update canary percentage (v1 + v2 = 100)
{ "type": "update_canary", "msg_id": 3,
  "service": "api", "percentage": 50 }
-> { "type": "canary_updated", "in_reply_to": 3,
    "service": "api", "v1": 50, "v2": 50 }

// Stable A/B assignment per user
{ "type": "assign_variant", "msg_id": 4, "user_id": "user-123" }
-> { "type": "variant_assigned", "in_reply_to": 4,
    "user_id": "user-123", "variant": "A" }
```

A/B variant assignment must be deterministic: the same user_id must always receive the same variant.

## Concepts

- canary deployment
- traffic splitting
- A/B testing
- blue-green deployment
- weighted routing

## Hints

- Weighted routing: pick a random number 0-99; route to v2 if < v2_percentage, else v1
- Header-based routing: check request headers for a match before falling back to weighted
- update_canary changes the v1/v2 split percentages; v1 + v2 must always sum to 100
- A/B test assignment: hash(user_id) % 2 gives a stable deterministic variant per user
- Header match takes priority over weighted split when both rules are active

## Test Cases

### 1. Weighted traffic split

Should route to v1 (80% weight).

Input:

```json
{"src":"client","dest":"proxy","body":{"type":"route","msg_id":1},"traffic_split":{"v1":80,"v2":20}}
```

Expected output:

```text
{"type": "routed", "in_reply_to": 1, "version": "v1", "reason": "weighted_routing"}
```

### 2. Header-based routing

x-beta header should route to v2.

Input:

```json
{"src":"client","dest":"proxy","body":{"type":"route","msg_id":1,"headers":{"x-beta":"true"}}}
```

Expected output:

```text
{"type": "routed", "in_reply_to": 1, "version": "v2", "reason": "header_match"}
```

## Resources

- [Canary Deployments](https://martinfowler.com/bliki/CanaryRelease.html): Gradual traffic shifting for safe production rollouts

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
