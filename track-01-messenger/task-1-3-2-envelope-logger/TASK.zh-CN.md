# 添加 消息 信封 日志器，包含Timestamps

英文标题：Add Message Envelope Logger，包含Timestamps
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-2-envelope-logger>

课程：1. 信使：消息通信基础
任务序号：12
短标题：信封 日志器
难度：intermediate
子主题：The Protocol Beneath

## 中文导读

本题要求你完成 `添加 消息 信封 日志器，包含Timestamps`。

重点关注：`logging`、`observability`、`message tracing`、`timestamps`。

建议先按提示逐步实现：日志 each 消息 as a single line，包含a timestamp prefix。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In production 分布式系统, **消息 tracing** is critical用于debugging. When something goes wrong, you need to answer: "What 消息 did this 节点 send和receive,和when?"

Your task is to add a 消息 envelope logger to your 节点:

1. Every received 消息 should be logged with: timestamp, direction (RECV), src, dest, body type
2. Every sent 消息 should be logged with: timestamp, direction (SENT), src, dest, body type
3. Logs are stored in an in-memory buffer (most recent 100 entries)
4. Implement a `get_log` 消息 type that returns the 日志 entries

```JSON
请求:  {"type": "get_log", "msg_id": 1, "count": 5}
响应: {"type": "get_log_ok", "in_reply_to": 1, "entries": [
    {"ts": "2024-01-01T00:00:00", "dir": "RECV", "src": "c0", "dest": "n1", "msg_type": "init"},
    {"ts": "2024-01-01T00:00:00", "dir": "SENT", "src": "n1", "dest": "c0", "msg_type": "init_ok"}
]}
```

The `count` field specifies how many recent entries to return. If fewer entries exist, return all of them.

## 涉及概念

- `logging`
- `observability`
- `message tracing`
- `timestamps`

## 实现提示

- 日志 each 消息 as a single line，包含a timestamp prefix
- Include direction (SENT or RECV), src, dest,和body type
- Use ISO 8601 format用于timestamps
- 日志 to 标准错误 so it does not interfere，包含标准输出 消息 passing
- Implement a get_log 消息 type that returns recent 日志 entries

## 测试用例

### 1. 初始化和回声 produce correct output

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"log-test"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "log-test", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Get 日志 returns entries after 初始化

The second output line is a get_log_ok，包含entries containing RECV init, SENT init_ok,和RECV get_log. Exact timestamps vary so only structure is checked.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"get_log","msg_id":2,"count":10}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Distributed Tracing](https://opentelemetry.io/docs/concepts/observability-primer/)：OpenTelemetry primer on observability in 分布式系统

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
