# Compare 2PC vs 3PC Protocols

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-4-comparison>

Track: 9. The Coordinator
Task order: 9
Short title: 2PC vs 3PC Comparison
Difficulty: intermediate
Subtrack: Three-Phase Commit (3PC)

## Problem

Understanding the trade-offs between 2PC and 3PC helps choose the right protocol for your use case.

**Message complexity**:
```
2PC (happy path):
  Prepare → 2N messages (N requests, N replies)
  Commit  → 2N messages (N requests, N replies)
  Total: 4N messages

3PC (happy path):
  CanCommit → 2N messages
  PreCommit  → 2N messages
  DoCommit   → 2N messages
  Total: 6N messages
```

**Blocking scenarios**:
```
2PC blocks when:
  - Coordinator crashes after collecting all Yes votes
  - Participant crashes after voting Yes but before receiving decision

3PC blocks when:
  - Coordinator crashes before sending PreCommit
  - Network partition separates coordinator from participants before PreCommit
  - (Does NOT block if coordinator crashes after PreCommit)
```

**Real-world usage**:
- **2PC**: Widely used (XA transactions, databases, message queues)
- **3PC**: Rarely used due to complexity and remaining blocking scenarios
- **Consensus-based**: Paxos/Raft are preferred for non-blocking commit

**Performance comparison**:
```json
Request:  {"type": "benchmark", "msg_id": 1, "protocols": ["2pc", "3pc"], "participants": 5, "transactions": 100}
Response: {"type": "benchmark_ok", "in_reply_to": 1, "results": {"2pc": {"avg_latency_ms": 45, "throughput_tps": 2200}, "3pc": {"avg_latency_ms": 68, "throughput_tps": 1450}}}
```

**When to use each**:
- **Use 2PC**: Simple, widely supported, acceptable blocking risk
- **Use 3PC**: Need slightly better availability, can tolerate extra complexity
- **Use consensus**: Need true non-blocking commit, can tolerate higher latency

## Concepts

- protocol comparison
- message complexity
- blocking scenarios
- real-world usage
- performance trade-offs

## Hints

- 2PC: 2 rounds (Prepare + Commit/Abort), 3PC: 3 rounds (CanCommit + PreCommit + DoCommit)
- 2PC blocks if coordinator crashes after Prepare, 3PC blocks if coordinator crashes before PreCommit
- 3PC reduces but doesn't eliminate blocking
- 3PC is rarely used in practice due to complexity and remaining blocking scenarios
- Most systems use 2PC or consensus-based approaches (Paxos/Raft)

## Test Cases

### 1. Benchmark 2PC vs 3PC latency

benchmark_ok should show 2PC has lower latency than 3PC due to fewer message rounds.

Input:

```json
{"src":"c0","dest":"benchmarker","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"]}}
{"src":"c1","dest":"benchmarker","body":{"type":"benchmark","msg_id":2,"protocols":["2pc","3pc"],"participants":3,"transactions":100}}
```

Expected output:

```text
{"src": "benchmarker", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compare blocking scenarios

compare_blocking_ok should return a table showing 2PC has 2 blocking scenarios, 3PC has 1.

Input:

```json
{"src":"c0","dest":"comparator","body":{"type":"init","msg_id":1}}
{"src":"c1","dest":"comparator","body":{"type":"compare_blocking","msg_id":2,"protocols":["2pc","3pc"]}}
```

Expected output:

```text
{"src": "comparator", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Two-Phase Commit vs Three-Phase Commit](https://martin.kleppmann.com/2018/09/24/two-phase-commit.html): Blog post comparing 2PC and 3PC by Martin Kleppmann

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
