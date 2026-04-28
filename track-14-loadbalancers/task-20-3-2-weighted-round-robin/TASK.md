# Implement Weighted Round-Robin Load Balancing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-2-weighted-round-robin>

Track: 14. Load Balancers
Task order: 12
Short title: Weighted Round-Robin
Difficulty: intermediate
Subtrack: Advanced Balancing Algorithms

## Problem

**Why weighted round-robin?**. ```. Problem: backends have different capacities. backend-1: 8 cores, 32GB RAM (high capacity). backend-2: 8 cores, 32GB RAM (high capacity). backend-3: 2 cores, 8GB RAM (low capacity). Standard round-robin sends 33% to each:. - backend-3 gets overwhelmed. - backend-1 and backend-2 underutilized. Weighted round-robin (weights: 4, 4, 2):. - backend-1: 40% of traffic. - backend-2: 40% of traffic. - backend-3: 20% of traffic. - Matches capacity ratios. ```. **Smooth weighted round-robin algorithm**:. ```typescript. name: string,. weight: number,. currentWeight: number. let maxBackend = null;. let maxWeight = -Infinity;. let totalWeight = 0;. // Add weight to each backend's current weight. backend.currentWeight += backend.weight;. totalWeight += backend.weight;. maxWeight = backend.currentWeight;. maxBackend = backend.name;. // Subtract total weight from selected backend. maxBackend.currentWeight -= totalWeight;. return maxBackend.name;. ```. **Example weighted routing**:. ```json. // Configuration:. "backends": [. ]. // Request sequence (first 10 requests):. Request: 1 → api-1. Request: 2 → api-2. Request: 3 → api-1. Request: 4 → api-2. Request: 5 → api-1. Request: 6 → api-2. Request: 7 → api-1. Request: 8 → api-2. Request: 9 → api-3 (20% traffic). Request: 10 → api-3. // Distribution: api-1: 40%, api-2: 40%, api-3: 20%. ```

## Concepts

- weighted round-robin
- capacity-based routing
- backend weights
- heterogeneous clusters
- traffic proportionality

## Hints

- Assign weights to backends based on capacity (e.g., CPU, memory)
- Higher weight = proportionally more requests
- Weights 4, 4, 2 means 40%, 40%, 20% traffic distribution
- Use a smooth weighted round-robin algorithm
- Handle weight changes dynamically without disruption

## Test Cases

### 1. Weight-based distribution

10 requests should distribute as: api-1: 4, api-2: 4, api-3: 2 (40%, 40%, 20%).

Input:

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":[{"name":"api-1","weight":4},{"name":"api-2","weight":4},{"name":"api-3","weight":2}],"algorithm":"weighted-round-robin"}}
{"src":"client","dest":"lb","body":{"type":"send_requests","msg_id":2,"count":10}}
```

Expected output:

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Unequal weights

14 requests should distribute as: large: 10, medium: 3, small: 1 (71%, 21%, 7%).

Input:

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":[{"name":"large","weight":10},{"name":"medium","weight":3},{"name":"small","weight":1}],"algorithm":"weighted-round-robin"}}
{"src":"client","dest":"lb","body":{"type":"send_requests","msg_id":2,"count":14}}
```

Expected output:

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

## Resources

- [Weighted Round-Robin DNS](https://www.nginx.com/blog/nginx-load-balancing-algorithms/): NGINX weighted load balancing documentation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
