# 验证混合逻辑时钟在误差范围内保持因果性

英文标题：Prove HLC Preserves Causality Within Epsilon
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-2-hlc-causality-bound>

课程：16. 时间守卫：逻辑时钟
任务序号：17
短标题：HLC 因果性边界
难度：高级
子主题：混合逻辑时钟

## 中文导读

本题要求你验证混合逻辑时钟的一个关键特性：它既能保持因果顺序，又能保证与物理时间的偏差不超过一个有界值。这正是 CockroachDB 等系统能够安全使用 HLC 的理论基础。你还需要处理物理时钟发生 NTP 校正（时钟回拨）的场景，验证 HLC 在这种情况下依然只进不退。

## 题目说明

混合逻辑时钟有一个至关重要的特性：它既能保持因果性，又能将与物理时间的偏差控制在一个有界的距离（即 epsilon）之内。正是这个特性使得 CockroachDB 等系统能够在实际中使用它。

需要验证的性质：
1. **因果性**：如果事件 A 先于事件 B 发生，那么 `hlc(A) < hlc(B)`
2. **有界偏移**：`|hlc.pt - wall_clock| <= epsilon`（使用 epsilon = 250 毫秒）
3. **NTP 校正容错**：即使物理时钟发生回拨，HLC 也只会向前推进

请实现一个 `hlc_verify_bound` 处理器，用于检查 epsilon 不变量：

```json
Request:  {"type": "hlc_verify_bound", "msg_id": 1, "epsilon_ms": 250}
Response: {"type": "hlc_verify_bound_ok", "in_reply_to": 1, "within_bound": true, "max_drift_ms": 0}
```

同时实现一个 `hlc_ntp_correction` 处理器，模拟物理时钟的回拨：

```json
Request:  {"type": "hlc_ntp_correction", "msg_id": 2, "old_wall_ms": 2000, "new_wall_ms": 1900}
Response: {"type": "hlc_ntp_correction_ok", "in_reply_to": 2, "hlc_pt": 2000, "hlc_c": 1, "moved_backward": false}
```

## 涉及概念

- `causality preservation`
- `clock skew bound`
- `NTP correction`
- `epsilon bound`

## 实现提示

- HLC 始终向前推进，即使物理时钟发生回拨也不会后退
- 逻辑计数器 c 是有界的，因为物理时间分量 pt 最终会赶上来
- 时钟偏移上界 epsilon 限制了 HLC 偏离真实时间的最大距离
- 通过发送回拨的墙钟时间值来模拟 NTP 校正
- 验证 HLC 时间戳始终保持在真实墙钟时间的 epsilon 范围之内

## 测试用例

### 1. 正常事件后 HLC 保持在 epsilon 范围内

`hlc_verify_bound_ok` 应显示 within_bound 为 true，max_drift_ms 为 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2,"wall_clock_ms":1000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":3,"wall_clock_ms":1100}}
{"src":"c1","dest":"n1","body":{"type":"hlc_verify_bound","msg_id":4,"epsilon_ms":250}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. NTP 回拨校正不会导致 HLC 后退

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2,"wall_clock_ms":2000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_ntp_correction","msg_id":3,"old_wall_ms":2000,"new_wall_ms":1900}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 2000, "c": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_ntp_correction_ok", "in_reply_to": 3, "hlc_pt": 2000, "hlc_c": 1, "moved_backward": false, "msg_id": 2}}
```

## 参考资料

- [CockroachDB Architecture - Clock Synchronization](https://www.cockroachlabs.com/docs/stable/architecture/transaction-layer.html)：介绍 CockroachDB 如何使用 HLC 实现分布式事务排序

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
