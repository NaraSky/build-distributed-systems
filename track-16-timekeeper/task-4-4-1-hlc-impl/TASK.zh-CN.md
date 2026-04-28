# 实现混合逻辑时钟

英文标题：Implement Hybrid Logical Clocks
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-1-hlc-impl>

课程：16. 时间守卫：逻辑时钟
任务序号：16
短标题：混合逻辑时钟实现
难度：进阶
子主题：混合逻辑时钟

## 中文导读

本题要求你实现混合逻辑时钟（Hybrid Logical Clock，简称 HLC）。HLC 融合了物理时钟和逻辑时钟的优点：既能保持与真实时间的接近，又能保证因果顺序。CockroachDB 和 Spanner 等知名分布式数据库都采用了这种时钟方案。掌握 HLC 是理解现代分布式数据库时间管理的关键。

## 题目说明

混合逻辑时钟（Hybrid Logical Clock，简称 HLC）结合了物理时钟（贴近真实时间）和逻辑时钟（保证因果顺序）两者的优点，被 CockroachDB 和 Spanner 等系统广泛使用。

HLC 的格式为 `(pt, c)`，其中：
- `pt`：物理时间，以毫秒为单位
- `c`：逻辑计数器（有界的，当 pt 推进时会重置）

更新规则：
- **本地事件或发送事件**：`pt_new = max(pt_local, pt_now)`。如果 `pt_new == pt_local`，则 `c += 1`；否则 `c = 0`。最后更新 `pt_local = pt_new`。
- **接收事件**：`pt_new = max(pt_local, pt_msg, pt_now)`。根据哪些 pt 值相等来调整 c 的值。

请实现以下处理器：

```json
Request:  {"type": "hlc_tick", "msg_id": 1, "wall_clock_ms": 1000}
Response: {"type": "hlc_tick_ok", "in_reply_to": 1, "pt": 1000, "c": 0}

Request:  {"type": "hlc_tick", "msg_id": 2, "wall_clock_ms": 1000}
Response: {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1000, "c": 1}

Request:  {"type": "hlc_tick", "msg_id": 3, "wall_clock_ms": 1005}
Response: {"type": "hlc_tick_ok", "in_reply_to": 3, "pt": 1005, "c": 0}

Request:  {"type": "hlc_recv", "msg_id": 4, "wall_clock_ms": 1003, "remote_pt": 1010, "remote_c": 3}
Response: {"type": "hlc_recv_ok", "in_reply_to": 4, "pt": 1010, "c": 4}
```

## 涉及概念

- `hybrid logical clock`
- `physical time`
- `logical counter`
- `CockroachDB`

## 实现提示

- HLC 是一个二元组 (pt, c)，其中 pt 是物理时间（毫秒），c 是逻辑计数器
- 本地或发送事件：如果当前墙钟时间 pt_now 大于 pt_local，则更新 pt_local 为 pt_now，c 重置为 0；否则递增 c
- 接收事件：pt_local 取本地 pt、消息 pt 和当前墙钟时间三者的最大值。如果 pt_local 没有变化，递增相应的 c
- HLC 始终向前推进，即使物理时钟发生倒退也不会后退
- 逻辑计数器 c 在物理时间分量推进时会重置为 0

## 测试用例

### 1. 首次事件使用墙钟时间

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

### 2. 相同墙钟时间下递增逻辑计数器

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

- [Logical Physical Clocks and Consistent Snapshots](https://cse.buffalo.edu/tech-reports/2014-04.pdf)：Kulkarni 等人提出的 HLC 原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
