# 实现 回调 清理器用于Leaked RPCs

英文标题：Implement Callback Reaper用于Leaked RPCs
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-4-callback-reaper>

课程：1. 信使：消息通信基础
任务序号：9
短标题：回调 清理器
难度：intermediate
子主题：RPC和the Request-Response模式l

## 中文导读

本题要求你完成 `实现 回调 清理器用于Leaked RPCs`。

重点关注：`resource cleanup`、`memory leaks`、`periodic tasks`、`garbage collection`。

建议先按提示逐步实现：Store the timestamp when each callback is registered。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a 节点 sends an async RPC but the recipient crashes or the 网络 drops the 消息, the callback stays in memory forever. This is a **resource leak** that can eventually consume all available memory.

Your task is to implement a **callback reaper** that:

1. Records the timestamp when each callback is registered
2. Periodically scans用于callbacks older than a threshold (default: 2 seconds)
3. Removes expired callbacks和invokes them，包含a 超时 error
4. Reports how many callbacks were reaped

Implement a `pending_count` 消息 type that returns the number of currently pending callbacks:

```JSON
请求:  {"type": "pending_count", "msg_id": 1}
响应: {"type": "pending_count_ok", "in_reply_to": 1, "count": 5}
```

Also implement a `send_fire_forget` 消息 type that sends an RPC without expecting a reply (to simulate leaked callbacks):

```JSON
请求:  {"type": "send_fire_forget", "msg_id": 1, "target": "n2", "payload": {"type": "echo", "echo": "lost"}}
响应: {"type": "send_fire_forget_ok", "in_reply_to": 1, "pending": 1}
```

## 涉及概念

- `resource cleanup`
- `memory leaks`
- `periodic tasks`
- `garbage collection`

## 实现提示

- Store the timestamp when each callback is registered
- Periodically scan the callbacks dictionary用于expired entries
- Use time.time() to get the current timestamp in seconds
- A reaper interval of 500ms is a good starting point
- When reaping, invoke the callback，包含an error or None to signal 超时

## 测试用例

### 1. Pending count starts at zero

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pending_count","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "pending_count_ok", "count": 0, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Fire-and-forget increases pending count

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"send_fire_forget","msg_id":2,"target":"n2","payload":{"type":"echo","echo":"lost"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "echo", "echo": "lost", "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "send_fire_forget_ok", "pending": 1, "in_reply_to": 2, "msg_id": 2}}
```

## 参考资料

- [Resource Leaks in Distributed Systems](https://sre.google/sre-book/handling-overload/)：Google SRE book chapter on managing resource limits和overload

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
