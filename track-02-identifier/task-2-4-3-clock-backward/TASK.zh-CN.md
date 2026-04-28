# HLC Handles Backward 时钟 Gracefully

英文标题：HLC Handles Backward Clock Gracefully
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-3-clock-backward>

课程：2. 标识符：分布式唯一 ID
任务序号：18
短标题：时钟 Backward
难度：advanced
子主题：混合逻辑 Clocks (HLC)

## 中文导读

本题要求你完成 `HLC Handles Backward 时钟 Gracefully`。

重点关注：`NTP adjustment`、`clock backward`、`monotonic guarantee`、`HLC resilience`。

建议先按提示逐步实现：When system 时钟 goes backward, HLC keeps its pt和increments lc。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

NTP can adjust the system 时钟 backward. Physical timestamps break. Lamport clocks keep working but lose time correlation. HLC handles it gracefully by keeping its physical component和incrementing the logical 计数器.

Implement a simulation that demonstrates this:

1. `simulate_clock_backward` sets the HLC's internal notion of "now" backward by a given amount
2. After the backward jump, HLC.tick() should still produce advancing timestamps
3. Report the drift between HLC.pt和actual physical time

```JSON
请求:  {"type": "simulate_backward", "msg_id": 1, "offset_ms": -5000}
响应: {"type": "simulate_backward_ok", "in_reply_to": 1}
```

Then tick和observe HLC advances despite backward 时钟:
```JSON
请求:  {"type": "hlc_tick", "msg_id": 2}
响应: {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1234567, "lc": 1, "drift_ms": 5000}
```

The `drift_ms` field shows how far HLC.pt is ahead of the (simulated) physical 时钟.

## 涉及概念

- `NTP adjustment`
- `clock backward`
- `monotonic guarantee`
- `HLC resilience`

## 实现提示

- When system 时钟 goes backward, HLC keeps its pt和increments lc
- This means HLC never goes backward, preserving ordering
- Lamport clocks also handle this, but lose physical time correlation
- Physical clocks break entirely on backward adjustments
- Track the drift between HLC.pt和actual physical time

## 测试用例

### 1. Simulate backward responds ok

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_backward","msg_id":2,"offset_ms":-5000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "simulate_backward_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Tick after backward still advances

After first tick (pt=now), simulate -10s backward. Second tick should keep same pt和increment lc,，包含drift_ms > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"simulate_backward","msg_id":3,"offset_ms":-10000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [NTP和Clock Synchronization](https://en.wikipedia.org/wiki/Network_Time_Protocol)：Overview of NTP和why 时钟 backward jumps happen

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
