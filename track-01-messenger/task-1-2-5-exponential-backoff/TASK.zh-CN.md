# 实现 指数退避用于Retries

英文标题：Implement Exponential Backoff用于Retries
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-5-exponential-backoff>

课程：1. 信使：消息通信基础
任务序号：10
短标题：指数退避
难度：intermediate
子主题：RPC和the Request-Response模式l

## 中文导读

本题要求你完成 `实现 指数退避用于Retries`。

重点关注：`exponential backoff`、`jitter`、`congestion control`、`load management`。

建议先按提示逐步实现：Base delay doubles，包含each attempt: delay = base_delay * 2^attempt。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Fixed-interval retries can overwhelm a recovering system. When many 节点 重试 at the same interval, they create a **thundering herd** that prevents recovery. **Exponential backoff** spreads retries over time.

Your task is to implement `rpc_with_backoff` that:

1. On the first attempt, waits `base_delay` (default: 100ms) before retrying
2. On each subsequent attempt, doubles the delay: `delay = base_delay * 2^attempt`
3. Adds random jitter: `delay += random(0, delay * 0.1)` to decorrelate retries
4. Caps the total delay at `max_delay` (default: 2 seconds)
5. Gives up after `max_retries` attempts (default: 5)

Implement a `backoff_relay` 消息 type:

```JSON
请求:  {"type": "backoff_relay", "msg_id": 1, "target": "n2", "payload": {"type": "read"}}
响应: {"type": "backoff_relay_ok", "in_reply_to": 1, "attempts": 3, "total_delay_ms": 700}
```

The 响应 includes the number of attempts和total delay in milliseconds. For this task, focus on the backoff calculation logic. Your 节点 should output the computed delay schedule.

Write a comment in your code explaining why exponential backoff helps under high load (at least 100 words).

## 涉及概念

- `exponential backoff`
- `jitter`
- `congestion control`
- `load management`

## 实现提示

- Base delay doubles，包含each attempt: delay = base_delay * 2^attempt
- Add random jitter to prevent thundering herd: delay += random(0, delay * 0.5)
- Cap the maximum delay to prevent unreasonably long waits
- 日志 each 重试，包含the computed delay用于observability
- The total wait time is the sum of all delays, not just the last one

## 测试用例

### 1. 初始化和回声 still work

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"backoff"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "backoff", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Compute backoff returns schedule

The 节点 should respond，包含a compute_backoff_ok containing schedule_ms array, total_ms,和retries. Due to jitter the exact values vary, but the 响应 structure must be correct.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compute_backoff","msg_id":2,"max_retries":3,"base_delay":0.1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)：AWS Architecture Blog on backoff strategies，包含detailed analysis
- [TCP Congestion Control](https://en.wikipedia.org/wiki/TCP_congestion_control)：How TCP uses exponential backoff用于congestion avoidance

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
