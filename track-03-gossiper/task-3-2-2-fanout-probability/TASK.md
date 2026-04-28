# Calculate Minimum Fanout for Reliable Delivery

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-2-fanout-probability>

Track: 3. The Gossiper
Task order: 7
Short title: Fanout Probability
Difficulty: advanced
Subtrack: Gossip Protocol

## Problem

What fanout K guarantees that all N nodes receive a message with probability >= 0.99? The theory says that after R rounds of gossip with fanout K, the probability that a specific node has NOT received the message is approximately (1 - K/N)^R.

Your task is to:
1. Implement the probability calculation: P(miss) = (1 - K/(N-1))^R
2. Find minimum K for a given N and target probability
3. Simulate gossip rounds to verify empirically

Implement a `calc_fanout` handler:
```json
Request:  {"type": "calc_fanout", "msg_id": 1, "nodes": 25, "target_prob": 0.99, "rounds": 5}
Response: {"type": "calc_fanout_ok", "in_reply_to": 1, "min_fanout": 3, "miss_prob": 0.003}
```

And a `simulate_gossip` handler that runs a Monte Carlo simulation:
```json
Request:  {"type": "simulate_gossip", "msg_id": 2, "nodes": 25, "fanout": 2, "rounds": 10, "trials": 100}
Response: {"type": "simulate_gossip_ok", "in_reply_to": 2, "delivery_rate": 0.98, "avg_rounds_to_all": 4.7}
```

## Concepts

- probability
- gossip reliability
- fanout analysis
- convergence

## Hints

- Probability of a node NOT receiving a message in one round: (1 - K/N)^R where R is rounds
- For 99% delivery across N nodes, solve for K given the number of gossip rounds
- More rounds = lower K needed, but more latency
- Log(N) rounds with fanout K=2 typically suffices for high probability delivery
- Implement a simulation to verify the theoretical formula empirically

## Test Cases

### 1. Calculate fanout for small cluster

calc_fanout_ok should have min_fanout >= 1 and miss_prob < 0.01.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"calc_fanout","msg_id":2,"nodes":5,"target_prob":0.99,"rounds":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Simulate gossip returns delivery rate

simulate_gossip_ok should have delivery_rate between 0 and 1, and avg_rounds_to_all > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_gossip","msg_id":2,"nodes":10,"fanout":3,"rounds":5,"trials":50}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Gossip Protocols - Cornell](https://www.cs.cornell.edu/courses/cs6410/2020fa/slides/22-gossip.pdf): Cornell lecture on gossip protocol analysis and convergence

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
