# Gossip PN-Counter Across a Cluster

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-4-gossip-counter>

Track: 4. The Counter
Task order: 9
Short title: Gossip Counter
Difficulty: advanced
Subtrack: G-Counter and PN-Counter

## Problem

To replicate the PN-Counter across a cluster, each node periodically gossips its full state to random peers. This is an anti-entropy protocol that guarantees eventual convergence.

**Gossip protocol**:
1. Every 100ms, select 2 random peers from the node list
2. Send your full counter state (P vector + N vector) to those peers
3. When you receive a gossip message, merge the received state with your local state

**Convergence measurement**:
- Apply 1000 random increments across 5 nodes
- Measure the time from the last increment until all 5 nodes agree on the value
- Expected convergence: within a few gossip rounds (< 1 second with 100ms interval)

```json
Request:  {"type": "gossip_status", "msg_id": 1}
Response: {"type": "gossip_status_ok", "in_reply_to": 1, "local_value": 1000, "gossip_rounds": 42, "peers_synced": 4, "convergence_ms": 350}
```

## Concepts

- gossip protocol
- counter replication
- convergence time
- anti-entropy
- random peer selection

## Hints

- Each node gossips its full counter state (P and N vectors) to 2 random peers
- Gossip interval: every 100ms, select 2 random peers and send your state
- On receiving gossip: merge the received state with your local state
- After 1000 increments across 5 nodes, measure time until all nodes converge
- Convergence = all nodes report the same value for read()

## Test Cases

### 1. Gossip replicates counter state

gossip_status_ok should show local_value >= 1 and gossip_rounds >= 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":1}}
{"src":"c1","dest":"n1","body":{"type":"gossip_status","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Remote increments are visible after gossip

After receiving gossip from n2, read should include n2 increments.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"n2","dest":"n1","body":{"type":"replicate","msg_id":2,"p_counters":{"n1":0,"n2":10},"n_counters":{"n1":0,"n2":0}}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Gossip Protocols](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/2007PromisesLimitations.pdf): Demers et al. - Epidemic algorithms for replicated database maintenance

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
