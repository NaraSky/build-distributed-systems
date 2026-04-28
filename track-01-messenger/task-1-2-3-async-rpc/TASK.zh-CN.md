# 基于回调实现异步 RPC

英文标题：Implement Async RPC Using Callbacks
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-3-async-rpc>

课程：1. 信使：消息通信基础
任务序号：8
短标题：异步 RPC
难度：进阶
子主题：RPC 与请求-响应模型

## 中文导读

前面实现的同步 RPC 有一个问题：发送请求后必须阻塞等待回复，期间节点无法处理其他消息。在高吞吐的分布式系统中，这是不可接受的。

这道题让你实现**异步 RPC**：发送请求后立即返回，不阻塞；等回复到达时，通过预先注册的回调函数来处理。这是构建高性能分布式系统的关键模式。

## 题目说明

同步 RPC 在等待回复期间会阻塞调用方，导致节点在此期间无法处理其他消息。在高吞吐的分布式系统中，**异步 RPC** 是更好的选择。

你的任务是实现一个 `async_rpc` 方法，它需要：

1. 向目标节点发送消息
2. 以发出消息的 `msg_id` 为键，注册一个回调函数（Callback）
3. 立即返回（非阻塞）
4. 当回复到达时（通过 `in_reply_to` 匹配），调用对应的回调函数，并传入回复的 body

实现一个 `batch_echo`（批量回声）消息类型来验证该功能：节点收到一组字符串后，为每个字符串向自己发送一条 `echo` RPC（环回），并通过回调收集所有回复。当所有回复都收集完成后，将结果返回给调用方。

```json
Request:  {"type": "batch_echo", "msg_id": 1, "values": ["a", "b", "c"]}
Response: {"type": "batch_echo_ok", "in_reply_to": 1, "results": ["a", "b", "c"]}
```

在测试中，节点应该向自己发送 echo 请求（即 `src` 和 `dest` 都是本节点）。

## 涉及概念

- `asynchronous programming`
- `callbacks`
- `non-blocking I/O`
- `event-driven`

## 实现提示

- 用一个字典（Map）存储回调函数，以 `msg_id` 为键
- 当回复到达时，通过 `in_reply_to` 查找对应的回调并执行
- 回调函数应该接收回复的 body 作为参数
- 使用处理器映射表来分发不同类型的消息
- 异步 RPC 允许节点在等待回复的同时继续处理其他消息

## 测试用例

### 1. 初始化和回声仍然正常工作

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

### 2. 回调注册并发送 RPC

`async_rpc` 应该向自身发送一条 echo 消息。当回复在后续消息中到达时，触发回调。

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

- [Callback-Based Asynchronous Programming](https://en.wikipedia.org/wiki/Callback_(computer_programming))：回调编程模式的概述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
