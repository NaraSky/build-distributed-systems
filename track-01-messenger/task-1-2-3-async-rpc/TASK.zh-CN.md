# 实现 异步 RPC使用Callbacks

英文标题：Implement Async RPC使用Callbacks
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-3-async-rpc>

课程：1. 信使：消息通信基础
任务序号：8
短标题：异步 RPC
难度：intermediate
子主题：RPC和the Request-Response模式l

## 中文导读

本题要求你完成 `实现 异步 RPC使用Callbacks`。

重点关注：`asynchronous programming`、`callbacks`、`non-blocking I/O`、`event-driven`。

建议先按提示逐步实现：Store callbacks in a dictionary keyed by msg_id。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Synchronous RPC blocks the caller until a reply arrives, which prevents the 节点 from handling other 消息 during that time. In high-throughput 分布式系统, **asynchronous RPC** is preferred.

Your task is to implement an `async_rpc` method that:

1. Sends a 消息 to a target 节点
2. Registers a callback function keyed by the outgoing `msg_id`
3. Returns immediately (non-blocking)
4. When a reply arrives (with matching `in_reply_to`), invokes the callback，包含the reply body

Implement a `batch_echo` 消息 type: the 节点 receives a list of strings, sends an `echo` RPC用于each one to itself (loopback),和collects all replies使用callbacks. Once all replies are collected, respond，包含the results.

```JSON
请求:  {"type": "batch_echo", "msg_id": 1, "values": ["a", "b", "c"]}
响应: {"type": "batch_echo_ok", "in_reply_to": 1, "results": ["a", "b", "c"]}
```

For testing, the 节点 should echo to itself (src和dest are the same 节点).

## 涉及概念

- `asynchronous programming`
- `callbacks`
- `non-blocking I/O`
- `event-driven`

## 实现提示

- Store callbacks in a dictionary keyed by msg_id
- When a reply arrives, look up the callback by in_reply_to和invoke it
- The callback should receive the reply body as its argument
- Use a handler map to dispatch different 消息 types
- Async RPC allows the 节点 to continue processing other 消息 while waiting

## 测试用例

### 1. 初始化和回声 still work

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"async"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "async", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 回调 registration sends RPC

The async_rpc should send an echo 消息 to itself. The callback fires when the reply arrives in a subsequent 消息.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"batch_echo","msg_id":2,"values":["x"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n1", "body": {"type": "echo", "echo": "x", "msg_id": 1}}
```

## 参考资料

- [Callback-Based Asynchronous Programming](https://en.wikipedia.org/wiki/Callback_(computer_programming))：Overview of callback patterns in programming

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
