# 实现 超时和重试循环用于RPC

英文标题：Implement Timeout和Retry循环用于RPC
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-2-timeout-retry>

课程：1. 信使：消息通信基础
任务序号：7
短标题：超时 & 重试
难度：intermediate
子主题：RPC和the Request-Response模式l

## 中文导读

本题要求你完成 `实现 超时和重试循环用于RPC`。

重点关注：`timeout`、`retry logic`、`fault tolerance`、`at-least-once delivery`。

建议先按提示逐步实现：Wrap your sync_rpc in a loop that retries on 超时。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In 分布式系统, 消息 can be lost or delayed indefinitely. A single RPC call，包含a 超时 is not enough — you need a **重试 loop** to handle transient failures.

Your task is to implement a `rpc_with_retry` method that:

1. Sends an RPC to the target 节点
2. Waits用于a reply，包含a 超时 (default: 500ms)
3. If no reply arrives, retries the RPC (with a new msg_id)
4. Gives up after `max_retries` attempts (default: 3)
5. Returns the 响应 body on success, or None after all retries fail

Implement a `relay` 消息 type to test this: when your 节点 receives a `relay` 请求, it uses `rpc_with_retry` to forward a 消息 to the target 节点.

```JSON
请求:  {"type": "relay", "msg_id": 1, "target": "n2", "payload": {"type": "read"}}
响应: {"type": "relay_ok", "in_reply_to": 1, "attempts": 3, "result": {...}}
```

The 响应 should include the number of attempts made. If all retries fail, respond，包含an error:
```JSON
{"type": "error", "in_reply_to": 1, "code": 0, "text": "RPC failed after 3 attempts"}
```

## 涉及概念

- `timeout`
- `retry logic`
- `fault tolerance`
- `at-least-once delivery`

## 实现提示

- Wrap your sync_rpc in a loop that retries on 超时
- Track the number of attempts和give up after max_retries
- Each 重试 should use a new msg_id用于the outgoing 消息
- 日志 each 重试 attempt to 标准错误用于observability
- Return the first successful 响应 or an error after exhausting retries

## 测试用例

### 1. 初始化和回声 still work，包含重试 node

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

### 2. Relay emits outgoing RPC 消息

First 重试 attempt sends the RPC to n2. Subsequent retries may also emit 消息 but the test only checks first output.

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

- [Retry Patterns in Distributed Systems](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)：AWS Builders Library on 超时和重试 strategies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
