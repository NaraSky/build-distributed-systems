# Analyze CRDT Tradeoffs vs. OCC and Locking

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-4-crdt-tradeoffs>

Track: 4. The Counter
Task order: 14
Short title: CRDT Tradeoffs
Difficulty: intermediate
Subtrack: More CRDTs

## Problem

CRDTs provide coordination-free eventual consistency, but come with tradeoffs. Comparing CRDTs with OCC (Optimistic Concurrency Control) and locking reveals when each approach is appropriate.

**CRDT advantages**:
- Always available (no coordination required)
- Works under network partitions (AP in CAP)
- Automatic conflict resolution (no human intervention)

**CRDT disadvantages**:
- Storage overhead: tombstones, vector clocks, tags accumulate
- Merge complexity: custom merge functions for each data type
- Weaker consistency: only eventual (not linearizable)

**Comparison table**:
| Aspect | CRDT | OCC | Locking |
|--------|------|-----|---------|
| Consistency | Eventual | Linearizable | Linearizable |
| Availability | Always | Abort on conflict | Block on contention |
| Coordination | None | Validation phase | Lock acquisition |
| Storage | High (metadata) | Low | Low |
| Latency | Low (local) | Low (optimistic) | Variable (wait) |

```json
Request:  {"type": "tradeoff_analysis", "msg_id": 1, "use_case": "shopping_cart", "partition_rate": 0.1, "conflict_rate": 0.3}
Response: {"type": "tradeoff_analysis_ok", "in_reply_to": 1, "recommendation": "CRDT", "reasoning": "High partition rate favors always-available CRDT over blocking approaches"}
```

## Concepts

- CRDT tradeoffs
- storage overhead
- merge complexity
- OCC comparison
- coordination-free

## Hints

- CRDTs: no coordination, but tombstones and metadata increase storage cost
- Locking: strong consistency, but lock contention limits scalability
- OCC (Optimistic Concurrency Control): good for low-conflict workloads, aborts on conflict
- CRDTs shine under partition: they remain available without coordination
- Build a comparison for 3 use cases: counter, shopping cart, document editing

## Test Cases

### 1. High partition rate recommends CRDT

High partition rate should recommend CRDT.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tradeoff_analysis","msg_id":2,"use_case":"counter","partition_rate":0.5,"conflict_rate":0.1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Low conflict rate recommends OCC

Low partition + low conflict with strong consistency need should recommend OCC or Locking.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tradeoff_analysis","msg_id":2,"use_case":"banking","partition_rate":0.01,"conflict_rate":0.05}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [CRDTs in Practice](https://martin.kleppmann.com/2020/07/06/crdt-hard-parts-hydra.html): Kleppmann - CRDTs: The Hard Parts

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
