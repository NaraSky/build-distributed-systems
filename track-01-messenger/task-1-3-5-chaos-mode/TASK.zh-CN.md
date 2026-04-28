# 添加 混沌模式，包含Random 消息丢弃

英文标题：Add Chaos模式，包含Random Message丢弃
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-5-chaos-mode>

课程：1. 信使：消息通信基础
任务序号：15
短标题：混沌模式
难度：intermediate
子主题：The Protocol Beneath

## 中文导读

本题要求你完成 `添加 混沌模式，包含Random 消息丢弃`。

重点关注：`chaos engineering`、`fault injection`、`resilience testing`、`network partitions`。

建议先按提示逐步实现：Use a random number generator to decide whether to drop each outgoing 消息。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Real networks drop 消息. Netflix pioneered **chaos engineering** — deliberately injecting failures to test resilience. Your task is to add a "chaos mode" to your 节点.

When chaos mode is enabled, the 节点 randomly drops a configurable percentage of **outgoing** 消息 (does not send them to 标准输出). This simulates 网络 packet loss.

Implement these 消息 types:

1. `chaos_on` — Enable chaos mode，包含a given drop rate:
```JSON
请求:  {"type": "chaos_on", "msg_id": 1, "drop_rate": 0.1}
响应: {"type": "chaos_on_ok", "in_reply_to": 1, "drop_rate": 0.1}
```

2. `chaos_off` — Disable chaos mode:
```JSON
请求:  {"type": "chaos_off", "msg_id": 2}
响应: {"type": "chaos_off_ok", "in_reply_to": 2}
```

3. `chaos_stats` — Report chaos statistics:
```JSON
请求:  {"type": "chaos_stats", "msg_id": 3}
响应: {"type": "chaos_stats_ok", "in_reply_to": 3, "enabled": true, "drop_rate": 0.1, "total_sent": 50, "total_dropped": 5}
```

Use a fixed random seed (42)用于reproducibility in tests. The drop decision uses `random.random() < drop_rate`.

Chaos mode should NOT drop control 消息 (`init_ok`, `chaos_on_ok`, `chaos_off_ok`, `chaos_stats_ok`) — only application 消息 like `echo_ok`.

## 涉及概念

- `chaos engineering`
- `fault injection`
- `resilience testing`
- `network partitions`

## 实现提示

- Use a random number generator to decide whether to drop each outgoing 消息
- The drop rate should be configurable (default 10%)
- 日志 dropped 消息 to 标准错误 so you can observe chaos effects
- Track how many 消息 were dropped vs sent
- Chaos mode should be toggleable via a 消息

## 测试用例

### 1. 初始化和回声 work without 混沌

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"safe"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "safe", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 混沌 on responds，包含drop_rate

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chaos_on","msg_id":2,"drop_rate":0.5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "chaos_on_ok", "drop_rate": 0.5, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Principles of Chaos Engineering](https://principlesofchaos.org/)：The foundational document on chaos engineering methodology
- [Netflix Chaos Monkey](https://netflix.github.io/chaosmonkey/)：Netflix tool用于randomly terminating instances in production

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
