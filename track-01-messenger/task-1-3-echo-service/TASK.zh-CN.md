# 实现回声服务并正确响应

英文标题：Implement Echo Service with Proper Acknowledgment
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-echo-service>

课程：1. 信使：消息通信基础
任务序号：3
短标题：回声服务
难度：入门
子主题：Hello, Distributed World

## 中文导读

这道题让你实现一个最简单的"回声服务"：客户端发来一个值，你的节点原样返回。虽然功能简单，但它是分布式系统中最基础的请求-响应模式的体现。

你需要在上一题初始化处理的基础上，增加对 `echo` 消息的处理，让你的节点同时支持两种消息类型。

## 题目说明

回声（Echo）是 Maelstrom 中最简单的工作负载。客户端发送一条包含某个值的 `echo` 消息，你的节点需要把这个值原样返回。

请求格式：

```json
{
  "type": "echo",
  "msg_id": 1,
  "echo": "Please echo 35"
}
```

期望的响应格式：

```json
{
  "type": "echo_ok",
  "msg_id": 1,
  "in_reply_to": 1,
  "echo": "Please echo 35"
}
```

你需要把上一题实现的 `init` 处理逻辑和这里新增的 `echo` 处理逻辑结合起来，让节点能够同时处理这两种消息类型。

## 概念说明

### 远程过程调用（RPC）

回声服务是**远程过程调用（RPC）**的最简形式：客户端发送请求，等待服务端的响应。虽然看起来很简单，但这个模式是所有分布式通信的基础。

### 请求-响应模式

像 Raft 这样复杂的系统，本质上也是由大量的请求-响应交互组成的：

```text
Client                          Server
  |                               |
  |------- Request (echo) ------->|
  |                               |
  |<------ Response (echo_ok) ----|
  |                               |
```

### 消息分发

你的节点需要根据消息的 `type` 字段**将消息分发**到对应的处理函数。这个模式贯穿整个课程：

- 检查消息中的 `type` 字段
- 路由到正确的处理函数
- 生成并发送相应的响应

### 伪代码

```text
for each message from stdin:
    parse JSON
    switch message.body.type:
        case "init":
            store node_id and node_ids
            reply with init_ok
        case "echo":
            reply with echo_ok containing the echo value
        default:
            log unknown message type
```

### 幂等性

回声操作天然具有**幂等性（Idempotent）**——用相同的输入调用多次，结果完全一样。这个特性在分布式系统中非常有价值，因为消息可能会被重试。

打个比方：问某人"你叫什么名字"，不管问多少次，答案都是一样的——这就是幂等的。

## 涉及概念

- `RPC`
- `request-response`
- `message handling`

## 实现提示

- `echo` 消息中包含一个 `echo` 字段，里面是需要回传的值
- 响应消息的类型是 `echo_ok`
- 响应中要包含原始的 `echo` 值

## 测试用例

### 1. 回声响应

先处理初始化，再处理回声请求，将 `echo` 字段的值原样返回。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"hello"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "hello", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Echo Workload](https://fly.io/dist-sys/1/)：Fly.io Gossip Glomers 回声挑战的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
