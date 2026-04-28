# 创建 异步 事件循环用于Concurrent 消息处理

英文标题：Create Async Event循环用于Concurrent Message处理
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-5-async-handler>

课程：1. 信使：消息通信基础
任务序号：5
短标题：异步 处理器
难度：intermediate
子主题：Hello, Distributed World

## 中文导读

本题要求你完成 `创建 异步 事件循环用于Concurrent 消息处理`。

重点关注：`concurrency`、`event loop`、`async processing`。

建议先按提示逐步实现：Use threading or asyncio用于concurrent handling。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Real 分布式系统 handle many 消息 concurrently. Your current synchronous implementation processes one 消息 at a time, which limits throughput.

Refactor your 节点 to handle 消息 concurrently:

1. Read 消息 in the main thread
2. Dispatch each 消息 to a handler that runs concurrently
3. Ensure thread-safe access to shared state (node_id, counters, etc.)

This prepares you用于more complex workloads where you need to send 消息 while waiting用于responses.

## 概念说明

## Concurrency in Distributed Systems

分布式系统 are **inherently concurrent**. Multiple clients may send requests simultaneously,和your 节点 must handle them without blocking.

### Why Concurrency?

Consider a 节点 that:

  - Receives a 请求 that requires contacting another 节点

  - Must wait用于the 响应 before replying

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
       ，包含self.lock:
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
    Cooperative multitasking用于I/O-bound work
  
  
    **Actor模式l**
    Each entity has its own mailbox和processes messages sequentially
  

### Go's Approach

Go uses **goroutines** - lightweight threads managed by the Go runtime. Combined，包含channels, this makes concurrent programming more natural:

```text
// Launch a goroutine用于each message
go func() {
    handleMessage(msg)
}()
```

## 涉及概念

- `concurrency`
- `event loop`
- `async processing`

## 实现提示

- Use threading or asyncio用于concurrent handling
- Be careful，包含shared state
- Consider使用a 队列用于消息 processing
- Go tip: handle init synchronously before spawning goroutines用于other 消息
- Buffer output和sort by in_reply_to before printing to get deterministic msg_id ordering

## 测试用例

### 1.处理3 concurrent 回声 messages

All 3 echo 消息 should receive responses. Under concurrency msg_ids may vary.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"test1"}}
{"src":"c2","dest":"n1","body":{"type":"echo","msg_id":3,"echo":"test2"}}
{"src":"c3","dest":"n1","body":{"type":"echo","msg_id":4,"echo":"test3"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "test1", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c2", "body": {"type": "echo_ok", "echo": "test2", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c3", "body": {"type": "echo_ok", "echo": "test3", "in_reply_to": 4, "msg_id": 3}}
```

## 参考资料

- [Python Threading](https://docs.python.org/3/library/threading.html)：Python documentation on threading primitives
- [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html)：High-level interface用于asynchronously executing callables

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
