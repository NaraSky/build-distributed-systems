# 实现带超时的同步 RPC

英文标题：Implement Synchronous RPC with Timeout
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-1-sync-rpc>

课程：1. 信使：消息通信基础
任务序号：6
短标题：同步 RPC
难度：进阶
子主题：RPC 与请求-响应模型

## 中文导读

这道题让你实现分布式系统中最经典的通信模式——同步远程过程调用（Sync RPC）。简单来说，就是向另一个节点发送请求，然后阻塞等待对方的回复，超时后放弃。

你还需要实现一个 `proxy`（代理）消息类型来验证 RPC 功能：收到代理请求后，将内部消息转发给目标节点，等待回复后再返回给原始调用方。

## 题目说明

在分布式系统中，节点经常需要调用其他节点上的过程并等待结果，这就是**同步远程过程调用（RPC）**。

你的任务是为 Maelstrom 节点扩展一个 `sync_rpc` 方法，该方法需要：

1. 向另一个节点发送消息
2. 阻塞等待响应（通过 `in_reply_to` 字段匹配）
3. 返回响应的 body
4. 超过指定时间（默认 1 秒）后超时

节点仍然需要处理 `init` 和 `echo` 消息。此外，还需要实现一个 `proxy`（代理）消息类型：当节点收到 `proxy` 请求时，使用 `sync_rpc` 将内部消息转发给目标节点，等待回复后将结果返回给原始调用方。

```
Request:  {"type": "proxy", "msg_id": 1, "target": "n2", "inner": {"type": "echo", "echo": "hello"}}
Response: {"type": "proxy_ok", "in_reply_to": 1, "result": {"type": "echo_ok", "echo": "hello", ...}}
```

在本题的测试中，由于 Maelstrom 测试工具只发送单节点输入，你需要在本地模拟远程节点的响应。你的 `sync_rpc` 应该将待处理的回调存起来，当匹配的回复到达时再完成它。

## 涉及概念

- `RPC`
- `synchronous communication`
- `timeout`
- `blocking calls`

## 实现提示

- 使用一个字典（Map）来存储待处理的请求，以 `msg_id` 为键
- 使用 `threading.Event` 或简单的轮询来阻塞调用方
- 设置超时，避免调用方永远阻塞
- 当响应到达时，通过 `in_reply_to` 匹配对应的请求并解除阻塞
- 超时后返回 `null` 或抛出异常

## 测试用例

### 1. 初始化和回声仍然正常工作

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"hello"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "hello", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 代理转发 RPC 到目标节点

节点应该将内部消息通过 `sync_rpc` 转发给 n2。由于 n2 不存在，RPC 会超时，但发往 n2 的消息必须被输出。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"proxy","msg_id":2,"target":"n2","inner":{"type":"echo","echo":"test"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "echo", "echo": "test", "msg_id": 1}}
```

## 参考资料

- [Remote Procedure Calls in Distributed Systems](https://www.cs.cornell.edu/courses/cs5414/2017fa/lectures/lec-rpc.pdf)：康奈尔大学关于 RPC 语义和故障模式的讲义

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
