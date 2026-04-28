# 实现 混合逻辑 Clocks

英文标题：Implement Hybrid Logical Clocks
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-1-hlc-impl>

课程：16. 时间守卫：逻辑时钟
任务序号：16
短标题：HLC Implementation
难度：intermediate
子主题：混合逻辑 Clocks

## 中文导读

本题要求你完成 `实现 混合逻辑 Clocks`。

重点关注：`hybrid logical clock`、`physical time`、`logical counter`、`CockroachDB`。

建议先按提示逐步实现：HLC is a pair: (pt, c) where pt = physical time in ms, c = logical 计数器。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A Hybrid Logical 时钟 (HLC) combines the best of physical clocks (real-time proximity)和logical clocks (causal ordering). Used in CockroachDB和Spanner.

HLC format: `(pt, c)` where:
- `pt`: physical time in milliseconds
- `c`: logical 计数器 (bounded, resets when pt advances)

Rules:
- **Local/Send event**: `pt_new = max(pt_local, pt_now)`. If `pt_new == pt_local`, `c += 1`. Else `c = 0`. Set `pt_local = pt_new`.
- **Receive event**: `pt_new = max(pt_local, pt_msg, pt_now)`. Adjust c based on which pt values tied.

Implement handlers:

```JSON
请求:  {"type": "hlc_tick", "msg_id": 1, "wall_clock_ms": 1000}
响应: {"type": "hlc_tick_ok", "in_reply_to": 1, "pt": 1000, "c": 0}

请求:  {"type": "hlc_tick", "msg_id": 2, "wall_clock_ms": 1000}
响应: {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1000, "c": 1}

请求:  {"type": "hlc_tick", "msg_id": 3, "wall_clock_ms": 1005}
响应: {"type": "hlc_tick_ok", "in_reply_to": 3, "pt": 1005, "c": 0}

请求:  {"type": "hlc_recv", "msg_id": 4, "wall_clock_ms": 1003, "remote_pt": 1010, "remote_c": 3}
响应: {"type": "hlc_recv_ok", "in_reply_to": 4, "pt": 1010, "c": 4}
```

## 涉及概念

- `hybrid logical clock`
- `physical time`
- `logical counter`
- `CockroachDB`

## 实现提示

- HLC is a pair: (pt, c) where pt = physical time in ms, c = logical 计数器
- On local/send event: if pt_now > pt_local, set pt_local = pt_now, c = 0. Else increment c.
- On receive: pt_local = max(pt_local, pt_msg, pt_now). If pt_local stayed the same, increment appropriate c.
- HLC always moves forward, even if the physical 时钟 goes backward
- The logical 计数器 c resets to 0 whenever the physical component advances

## 测试用例

### 1. First tick uses wall 时钟

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2,"wall_clock_ms":1000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1000, "c": 0, "msg_id": 1}}
```

### 2. Same wall 时钟 ms increments logical 计数器

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2,"wall_clock_ms":1000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":3,"wall_clock_ms":1000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":4,"wall_clock_ms":1000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1000, "c": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 3, "pt": 1000, "c": 1, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 4, "pt": 1000, "c": 2, "msg_id": 3}}
```

## 参考资料

- [Logical Physical Clocks和Consistent Snapshots](https://cse.buffalo.edu/tech-reports/2014-04.pdf)：The original HLC paper by Kulkarni et al.

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
