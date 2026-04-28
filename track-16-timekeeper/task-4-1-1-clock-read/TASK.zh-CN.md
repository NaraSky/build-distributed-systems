# Read System 时钟和Detect Backward Jumps

英文标题：Read System Clock和Detect Backward Jumps
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-1-clock-read>

课程：16. 时间守卫：逻辑时钟
任务序号：1
短标题：时钟 Read
难度：intermediate
子主题：Physical Time和Its Failures

## 中文导读

本题要求你完成 `Read System 时钟和Detect Backward Jumps`。

重点关注：`system clock`、`clock monotonicity`、`NTP`、`backward jump`。

建议先按提示逐步实现：Use time.time()用于wall 时钟和time.monotonic()用于monotonic 时钟。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

System clocks can go backward due to NTP adjustments. Your task is to read the 时钟 repeatedly和detect backward jumps.

Implement a `clock_sample` handler that reads the 时钟 N times:
```JSON
请求:  {"type": "clock_sample", "msg_id": 1, "count": 100, "offset_ms": 0}
响应: {"type": "clock_sample_ok", "in_reply_to": 1, "samples": 100, "backward_jumps": 0, "max_delta_us": 15, "min_delta_us": 1}
```

Also implement `simulate_ntp` to inject a backward offset:
```JSON
请求:  {"type": "simulate_ntp", "msg_id": 2, "offset_ms": -50}
响应: {"type": "simulate_ntp_ok", "in_reply_to": 2}
```

## 涉及概念

- `system clock`
- `clock monotonicity`
- `NTP`
- `backward jump`

## 实现提示

- Use time.time()用于wall 时钟和time.monotonic()用于monotonic 时钟
- Compare consecutive readings to detect backward jumps
- NTP adjustments can cause the wall 时钟 to jump backward
- Track minimum和maximum deltas between readings
- Store readings in a buffer用于analysis

## 测试用例

### 1. 时钟 sample returns stats

clock_sample_ok should have samples=10和backward_jumps=0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"clock_sample","msg_id":2,"count":10}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Simulate NTP responds ok

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_ntp","msg_id":2,"offset_ms":-50}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "simulate_ntp_ok", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Falsehoods Programmers Believe About Time](https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time)：Common misconceptions about timekeeping in software

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
