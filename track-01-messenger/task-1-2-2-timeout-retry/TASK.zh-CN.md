# 实现 RPC 超时与重试机制

网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-2-timeout-retry>

课程：1. 信使：消息通信基础
任务序号：7
短标题：超时与重试
难度：进阶
子主题：RPC 与请求-响应模型

## 中文导读

在真实的分布式系统中，消息随时可能丢失或延迟。发一次请求然后干等着是行不通的，你必须有一套"发了没回就再发"的机制。

这道题让你在前面实现的同步 RPC 基础上，加入超时重试功能。核心思路很简单：发出请求后等一段时间，没收到回复就重发，直到成功或者放弃。这是分布式系统容错的基本功。

## 题目说明

在分布式系统中，消息可能丢失，也可能无限延迟。单次带超时的远程过程调用（RPC）并不够可靠，你需要在外面再套一个**重试循环**来应对这些暂时性的故障。

你的任务是实现一个 `rpc_with_retry` 方法，它的工作流程如下：

1. 向目标节点（Node）发送一次 RPC 请求
2. 等待对方的回复，超时时间默认为 500 毫秒
3. 如果超时没有收到回复，换一个新的 `msg_id` 重新发送请求
4. 达到最大重试次数（默认 3 次）后放弃
5. 成功时返回响应内容，所有重试都失败时返回 null

为了测试这个功能，你需要实现一个 `relay`（中继）消息类型：当你的节点收到 `relay` 请求时，调用 `rpc_with_retry` 把消息转发给目标节点。

```json
Request:  {"type": "relay", "msg_id": 1, "target": "n2", "payload": {"type": "read"}}
Response: {"type": "relay_ok", "in_reply_to": 1, "attempts": 3, "result": {...}}
```

响应中应包含实际尝试了多少次。如果所有重试都失败了，返回一条错误消息：

```json
{"type": "error", "in_reply_to": 1, "code": 0, "text": "RPC failed after 3 attempts"}
```

## 涉及概念

- `timeout`
- `retry logic`
- `fault tolerance`
- `at-least-once delivery`

## 实现提示

- 在同步 RPC 的外面套一个循环，超时后自动重试
- 记录每次尝试的次数，达到上限后停止
- 每次重试都要使用新的 `msg_id`，不能复用旧的
- 把每次重试的信息输出到标准错误（stderr），方便调试和观察
- 返回第一个成功的响应，或者在重试用完后返回错误

## 测试用例

### 1. 初始化和回声功能在重试节点中仍然正常工作

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"retry-test"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "retry-test", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 中继消息会发出 RPC 请求

第一次尝试会向 n2 发送 RPC 请求。后续的重试也可能产生输出消息，但测试只验证第一条输出。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"relay","msg_id":2,"target":"n2","payload":{"type":"read"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "read", "msg_id": 1}}
```

## 参考资料

- [Retry Patterns in Distributed Systems](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)：AWS 构建者库中关于超时、重试和退避策略的文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
