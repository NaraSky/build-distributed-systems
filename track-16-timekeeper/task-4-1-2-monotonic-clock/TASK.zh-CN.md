# 实现 Monotonic 时钟 Wrapper

英文标题：Implement Monotonic Clock Wrapper
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-2-monotonic-clock>

课程：16. 时间守卫：逻辑时钟
任务序号：2
短标题：Monotonic 时钟
难度：intermediate
子主题：Physical Time和Its Failures

## 中文导读

本题要求你完成 `实现 Monotonic 时钟 Wrapper`。

重点关注：`monotonic clock`、`clock wrapper`、`information loss`、`ordering guarantee`。

建议先按提示逐步实现：Wrap the system 时钟 to always return >= previous value。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A MonotonicClock wraps the system 时钟和guarantees the returned value never decreases. Implement this wrapper和track what information is lost.

```JSON
请求:  {"type": "mono_read", "msg_id": 1}
响应: {"type": "mono_read_ok", "in_reply_to": 1, "time_ms": 1234567, "corrections": 0}
```

## 涉及概念

- `monotonic clock`
- `clock wrapper`
- `information loss`
- `ordering guarantee`

## 实现提示

- Wrap the system 时钟 to always return >= previous value
- Use max(current, last_returned) as the strategy
- Track how many times the wrapper prevented a backward jump
- Information lost: you cannot detect when time actually went backward
- time.monotonic() in Python provides this natively

## 测试用例

### 1. Mono read returns time

mono_read_ok，包含time_ms > 0和corrections=0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Two reads are non-decreasing

Second time_ms >= first time_ms.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Monotonic Clocks](https://docs.python.org/3/library/time.html#time.monotonic)：Python docs on monotonic 时钟 guarantees

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
