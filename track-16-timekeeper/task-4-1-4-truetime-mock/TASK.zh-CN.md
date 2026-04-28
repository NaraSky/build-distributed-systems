# 实现 Mock TrueTime API

英文标题：Implement Mock TrueTime API
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-4-truetime-mock>

课程：16. 时间守卫：逻辑时钟
任务序号：4
短标题：TrueTime Mock
难度：advanced
子主题：Physical Time和Its Failures

## 中文导读

本题要求你完成 `实现 Mock TrueTime API`。

重点关注：`TrueTime`、`Google Spanner`、`uncertainty interval`、`bounded error`。

建议先按提示逐步实现：TrueTime returns [earliest, latest] instead of a single timestamp。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Google Spanner's TrueTime API returns a time interval instead of a point: `now() -> [earliest, latest]`. The true time is guaranteed to be within this interval.

Implement a mock TrueTime，包含configurable uncertainty:
```JSON
请求:  {"type": "truetime_now", "msg_id": 1}
响应: {"type": "truetime_now_ok", "in_reply_to": 1, "earliest": 1234560, "latest": 1234574, "uncertainty_ms": 7}

请求:  {"type": "set_uncertainty", "msg_id": 2, "uncertainty_ms": 10}
响应: {"type": "set_uncertainty_ok", "in_reply_to": 2}
```

## 涉及概念

- `TrueTime`
- `Google Spanner`
- `uncertainty interval`
- `bounded error`

## 实现提示

- TrueTime returns [earliest, latest] instead of a single timestamp
- The uncertainty window is typically ~7ms，包含GPS/atomic clocks
- earliest = now - uncertainty, latest = now + uncertainty
- Any event that happened at real time T has T within [earliest, latest]
- This is what Google Spanner uses用于external consistency

## 测试用例

### 1. TrueTime now returns interval

truetime_now_ok，包含earliest < latest和uncertainty_ms=7.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"truetime_now","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Set uncertainty

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"set_uncertainty","msg_id":2,"uncertainty_ms":20}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "set_uncertainty_ok", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Spanner: Google Globally-Distributed Database](https://research.google/pubs/pub39966/)：Original Spanner paper describing TrueTime

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
