# Optimize for High-Throughput ID Generation

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-5-high-throughput>

Track: 2. The Identifier
Task order: 5
Short title: High Throughput
Difficulty: intermediate
Subtrack: Why Unique IDs Are Hard

## Problem

Optimize your ID generator for maximum throughput. Real systems like Twitter generate millions of IDs per second. Your implementation should handle high concurrency without becoming a bottleneck.

Optimization strategies:

1. **Minimize lock contention** in multi-threaded scenarios
2. Use **atomic operations** where possible
3. Consider **pre-generating IDs** in batches
4. Profile and measure your throughput

**Target**: Handle 10,000+ ID generations per second on a single node.

## Concept Notes

## Throughput Optimization

ID generation is often on the **critical path**. Every database insert, every message, every event needs an ID. Even small inefficiencies multiply across millions of operations.

### Bottleneck Analysis

```text
def generate_id():
    with lock:           # ← Contention point
        timestamp = now()
        sequence += 1
        return id
```

Every concurrent request must acquire the same lock, serializing all ID generation.

### Optimization Techniques

  
    Technique
    Benefit
    Complexity
  
  
    Separate locks for msg_id and id_gen
    Reduces contention
    Low
  
  
    Atomic counters
    Lock-free increment
    Medium
  
  
    Pre-allocated ID ranges
    Batch amortization
    High
  

### Go's Advantage

Go's `sync/atomic` package provides lock-free primitives:

```text
import "sync/atomic"

var counter int64

func getNext() int64 {
    return atomic.AddInt64(&counter, 1)
}
```

This is significantly faster than mutex-based approaches under high contention.

## Concepts

- performance
- throughput
- optimization

## Hints

- Minimize lock contention
- Consider lock-free approaches
- Batch ID generation if possible

## Test Cases

### 1. Generate single ID

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
```

## Resources

- [Python Threading Best Practices](https://docs.python.org/3/library/threading.html): Python documentation on threading primitives
- [Go Atomic Operations](https://pkg.go.dev/sync/atomic): Go documentation on atomic operations for lock-free programming

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
