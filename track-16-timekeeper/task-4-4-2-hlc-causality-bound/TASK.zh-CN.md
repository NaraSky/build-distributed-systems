# Prove HLC Preserves Causality Within Epsilon

英文标题：Prove HLC Preserves Causality Within Epsilon
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-2-hlc-causality-bound>

课程：16. 时间守卫：逻辑时钟
任务序号：17
短标题：HLC Causality Bound
难度：advanced
子主题：混合逻辑 Clocks

## 中文导读

本题要求你完成 `Prove HLC Preserves Causality Within Epsilon`。

重点关注：`causality preservation`、`clock skew bound`、`NTP correction`、`epsilon bound`。

建议先按提示逐步实现：HLC always advances: it never goes backward even if physical 时钟 does。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

HLC has a critical property: it preserves causality AND stays within a bounded distance (epsilon) of physical time. This is what makes it practical用于systems like CockroachDB.

Properties to verify:
1. **Causality**: if event A happened-before event B, then `hlc(A) < hlc(B)`
2. **Bounded drift**: `|hlc.pt - wall_clock| <= epsilon` (use epsilon = 250ms)
3. **NTP resilience**: even if wall 时钟 jumps backward, HLC moves forward

Implement a `hlc_verify_bound` handler that checks the epsilon invariant:

```JSON
请求:  {"type": "hlc_verify_bound", "msg_id": 1, "epsilon_ms": 250}
响应: {"type": "hlc_verify_bound_ok", "in_reply_to": 1, "within_bound": true, "max_drift_ms": 0}
```

Also implement a `hlc_ntp_correction` handler that simulates a backward 时钟 jump:

```JSON
请求:  {"type": "hlc_ntp_correction", "msg_id": 2, "old_wall_ms": 2000, "new_wall_ms": 1900}
响应: {"type": "hlc_ntp_correction_ok", "in_reply_to": 2, "hlc_pt": 2000, "hlc_c": 1, "moved_backward": false}
```

## 涉及概念

- `causality preservation`
- `clock skew bound`
- `NTP correction`
- `epsilon bound`

## 实现提示

- HLC always advances: it never goes backward even if physical 时钟 does
- The logical 计数器 c is bounded because pt will eventually catch up
- Epsilon (时钟 skew bound) limits how far HLC can drift from real time
- Simulate NTP corrections by sending wall_clock_ms values that jump backward
- Verify that HLC timestamp always stays within epsilon of the real wall 时钟

## 测试用例

### 1. HLC stays within epsilon after normal ticks

hlc_verify_bound_ok should show within_bound: true和max_drift_ms: 0.

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

### 2. NTP backward correction does not move HLC backward

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

- [CockroachDB Architecture - Clock Synchronization](https://www.cockroachlabs.com/docs/stable/architecture/transaction-layer.html)：How CockroachDB uses HLC用于distributed 事务 ordering

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
