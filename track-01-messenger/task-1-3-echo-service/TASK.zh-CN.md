# 实现 回声 服务，包含正确的 确认响应

英文标题：Implement Echo Service，包含Proper Acknowledgment
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-echo-service>

课程：1. 信使：消息通信基础
任务序号：3
短标题：回声 服务
难度：beginner
子主题：Hello, Distributed World

## 中文导读

本题要求你完成 `实现 回声 服务，包含正确的 确认响应`。

重点关注：`RPC`、`request-response`、`message handling`。

建议先按提示逐步实现：Echo 消息 contain an "echo" field，包含the value to echo back。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The echo workload is the simplest Maelstrom workload. Clients send echo 消息 containing a value,和your 节点 must echo that value back.

请求 format:

```JSON
{
  "type": "echo",
  "msg_id": 1,
  "echo": "Please echo 35"
}
```

Expected 响应:

```JSON
{
  "type": "echo_ok",
  "msg_id": 1,
  "in_reply_to": 1,
  "echo": "Please echo 35"
}
```

Combine your init handling from the previous task，包含a new echo handler. Your 节点 should handle both 消息 types.

## 概念说明

## Remote Procedure Calls (RPC)

Echo is the simplest form of **RPC**: a 客户端 sends a 请求和expects a 响应. While trivial, this pattern forms the basis of all distributed communication.

### The Request-Response Pattern

Complex systems like Raft are built from many 请求-响应 interactions:

```text
Client                          Server
  |                               |
  |------- Request (echo) ------->|
  |                               |
  |<------ Response (echo_ok) ----|
  |                               |
```

### 处理器 Dispatch

Your 节点 needs to **dispatch 消息** to appropriate handlers based on type. This is a pattern you will use throughout:

  - Examine the 消息 `type` field

  - Route to the correct handler function

  - Generate和send the appropriate 响应

### Pseudocode

```text
for each message from stdin:
    parse JSON
    switch message.body.type:
        case "init":
            store node_id和node_ids
            reply，包含init_ok
        case "echo":
            reply，包含echo_ok containing the echo value
        default:
            log unknown message type
```

### Idempotency

Echo is naturally **idempotent** - calling it multiple times，包含the same input produces the same output. This property is valuable in 分布式系统 where 消息 may be retried.

## 涉及概念

- `RPC`
- `request-response`
- `message handling`

## 实现提示

- Echo 消息 contain an "echo" field，包含the value to echo back
- 响应 type is "echo_ok"
- Include the original echo value in your 响应

## 测试用例

### 1. 回声 response

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

- [Echo Workload](https://fly.io/dist-sys/1/)：Fly.io gossip Glomers Echo challenge walkthrough

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
