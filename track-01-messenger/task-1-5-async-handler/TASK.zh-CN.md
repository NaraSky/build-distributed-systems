# 创建异步事件循环实现并发消息处理

英文标题：Create Async Event Loop for Concurrent Message Handling
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-5-async-handler>

课程：1. 信使：消息通信基础
任务序号：5
短标题：异步处理器
难度：进阶
子主题：Hello, Distributed World

## 中文导读

前面的题目中，你的节点是一条一条依次处理消息的。但在真实的分布式系统中，消息会同时大量涌入，逐条处理会严重限制吞吐量。这道题要求你改造节点，让它能够并发处理多条消息。

这为后续更复杂的场景做准备——比如在等待其他节点的响应时，你的节点需要同时处理新到的请求。

## 题目说明

真实的分布式系统需要并发处理大量消息。你当前的同步实现一次只能处理一条消息，这会限制吞吐量。

现在需要重构你的节点，使其支持并发处理消息：

1. 在主线程中读取消息
2. 将每条消息分派给并发执行的处理器
3. 确保对共享状态（如 `node_id`、计数器等）的访问是线程安全的

## 概念说明

### 分布式系统中的并发

分布式系统**天生就是并发的**。多个客户端可能同时发送请求，你的节点必须在不阻塞的情况下处理它们。

### 为什么需要并发？

想象一个节点遇到这样的情况：

- 收到一个请求，需要先联系另一个节点才能处理
- 必须等待对方回复后才能响应
- 在等待期间，又有新的请求到来

如果没有并发，后续所有请求都会被**阻塞**，直到第一个请求处理完毕。这就像餐厅只有一个服务员，如果他去厨房等菜了，其他桌的客人就没人招待了。

### 线程安全

当多个线程访问共享状态时，必须使用**同步原语**（如锁）来防止竞态条件（Race Condition）。

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

### 常见的并发模式

| 模式 | 适用场景 |
|------|---------|
| **线程池（Thread Pool）** | 固定数量的工作线程处理一个任务队列 |
| **异步/等待（Async/Await）** | 适合 I/O 密集型任务的协作式多任务 |
| **Actor 模型** | 每个实体拥有自己的邮箱，按顺序处理消息 |

### Go 语言的做法

Go 使用 **goroutine** —— 由 Go 运行时管理的轻量级线程。结合 channel（通道），Go 让并发编程变得更加自然：

```text
// Launch a goroutine for each message
go func() {
    handleMessage(msg)
}()
```

## 涉及概念

- `concurrency`
- `event loop`
- `async processing`

## 实现提示

- 使用多线程或异步框架来并发处理消息
- 注意保护共享状态，避免竞态条件
- 可以考虑用队列来组织消息处理
- Go 语言提示：先同步处理 `init` 消息，再为其他消息启动 goroutine
- 可以先缓冲输出，按 `in_reply_to` 排序后再打印，以获得确定性的 `msg_id` 顺序

## 测试用例

### 1. 并发处理 3 条回声消息

3 条 echo 消息都应该收到响应。在并发环境下 `msg_id` 的顺序可能有所不同。

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

- [Python Threading](https://docs.python.org/3/library/threading.html)：Python 线程原语的官方文档
- [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html)：用于异步执行的高级接口

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
