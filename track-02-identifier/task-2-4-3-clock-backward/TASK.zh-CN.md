# 混合逻辑时钟优雅应对时钟回拨

英文标题：HLC Handles Backward Clock Gracefully
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-3-clock-backward>

课程：2. 标识符：分布式唯一 ID
任务序号：18
短标题：时钟回拨处理
难度：高级
子主题：Hybrid Logical Clocks (HLC)

## 中文导读

在真实环境中，NTP 时间同步可能导致系统时钟突然向后跳变，这会破坏依赖物理时间戳的系统。混合逻辑时钟能够优雅地处理这种情况——即使物理时钟回退，它也能保持时间戳单调递增。本题要求你模拟时钟回拨场景，验证混合逻辑时钟的容错能力。

## 题目说明

网络时间协议（NTP）可能会将系统时钟向后调整。这对不同的时钟方案影响各不相同：

- **物理时间戳**：直接失效，因为时间戳会"倒退"
- **Lamport 时钟**：能继续正常工作，但会失去与真实时间的关联性
- **混合逻辑时钟**：优雅应对——保持物理时间分量不变，通过递增逻辑计数器来保证单调性

打个比方：假设你的手表突然慢了 5 秒，混合逻辑时钟不会跟着调回去，而是在之前记录的时间上继续往后编号，从而保证所有的时间戳始终是递增的。

你需要实现一个模拟来演示这个特性：

1. `simulate_clock_backward` 将系统的"当前时间"向后偏移指定的毫秒数
2. 回拨之后，执行 `hlc_tick()` 仍然应该产生递增的时间戳
3. 报告混合逻辑时钟的物理时间分量与实际物理时间之间的偏移量

```json
请求:  {"type": "simulate_backward", "msg_id": 1, "offset_ms": -5000}
响应: {"type": "simulate_backward_ok", "in_reply_to": 1}
```

然后执行 tick，观察时钟回拨后混合逻辑时钟仍然在前进：
```json
请求:  {"type": "hlc_tick", "msg_id": 2}
响应: {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1234567, "lc": 1, "drift_ms": 5000}
```

其中 `drift_ms` 字段表示混合逻辑时钟记录的物理时间超前（模拟回拨后的）系统物理时钟多少毫秒。

## 涉及概念

- `NTP adjustment`
- `clock backward`
- `monotonic guarantee`
- `HLC resilience`

## 实现提示

- 当系统时钟发生回拨时，混合逻辑时钟保持当前的物理时间分量不变，仅递增逻辑计数器
- 这意味着混合逻辑时钟永远不会倒退，从而保证了排序的正确性
- Lamport 时钟也能应对时钟回拨，但会失去与物理时间的关联
- 纯物理时钟在发生回拨时会完全失效
- 需要跟踪混合逻辑时钟的物理时间分量与实际物理时间之间的偏移量

## 测试用例

### 1. 模拟回拨返回确认

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

### 2. 回拨后执行 tick 仍然保持递增

第一次 tick 后物理时间等于当前时间，然后模拟 -10 秒的回拨。第二次 tick 应该保持相同的物理时间分量并递增逻辑计数器，且 drift_ms 大于 0。

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

- [NTP and Clock Synchronization](https://en.wikipedia.org/wiki/Network_Time_Protocol)：网络时间协议概述，解释了为什么会发生时钟回拨

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
