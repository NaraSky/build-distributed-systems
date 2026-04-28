# Create Async Event Loop for Concurrent Message Handling

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-5-async-handler>

Track: 1. The Messenger
Task order: 5
Short title: Async Handler
Difficulty: intermediate
Subtrack: Hello, Distributed World

## Problem

Real distributed systems handle many messages concurrently. Your current synchronous implementation processes one message at a time, which limits throughput.

Refactor your node to handle messages concurrently:

1. Read messages in the main thread
2. Dispatch each message to a handler that runs concurrently
3. Ensure thread-safe access to shared state (node_id, counters, etc.)

This prepares you for more complex workloads where you need to send messages while waiting for responses.

## Concept Notes

## Concurrency in Distributed Systems

Distributed systems are **inherently concurrent**. Multiple clients may send requests simultaneously, and your node must handle them without blocking.

### Why Concurrency?

Consider a node that:

  - Receives a request that requires contacting another node

  - Must wait for the response before replying

  - Receives more requests while waiting

Without concurrency, all subsequent requests are **blocked** until the first completes. This creates a bottleneck.

### Thread Safety

When multiple threads access shared state, you must use **synchronization primitives** like locks to prevent race conditions.

```text
import threading

class Node:
    def __init__(self):
        self.lock = threading.Lock()
        self.next_msg_id = 0
    
    def get_next_id(self):
        with self.lock:
            id = self.next_msg_id
            self.next_msg_id += 1
            return id
```

### Common Patterns

  
    Pattern
    Use Case
  
  
    **Thread Pool**
    Fixed number of worker threads processing a queue
  
  
    **Async/Await**
    Cooperative multitasking for I/O-bound work
  
  
    **Actor Model**
    Each entity has its own mailbox and processes messages sequentially
  

### Go's Approach

Go uses **goroutines** - lightweight threads managed by the Go runtime. Combined with channels, this makes concurrent programming more natural:

```text
// Launch a goroutine for each message
go func() {
    handleMessage(msg)
}()
```

## Concepts

- concurrency
- event loop
- async processing

## Hints

- Use threading or asyncio for concurrent handling
- Be careful with shared state
- Consider using a queue for message processing
- Go tip: handle init synchronously before spawning goroutines for other messages
- Buffer output and sort by in_reply_to before printing to get deterministic msg_id ordering

## Test Cases

### 1. Handle 3 concurrent echo messages

All 3 echo messages should receive responses. Under concurrency msg_ids may vary.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"test1"}}
{"src":"c2","dest":"n1","body":{"type":"echo","msg_id":3,"echo":"test2"}}
{"src":"c3","dest":"n1","body":{"type":"echo","msg_id":4,"echo":"test3"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "test1", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c2", "body": {"type": "echo_ok", "echo": "test2", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c3", "body": {"type": "echo_ok", "echo": "test3", "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [Python Threading](https://docs.python.org/3/library/threading.html): Python documentation on threading primitives
- [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html): High-level interface for asynchronously executing callables

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
