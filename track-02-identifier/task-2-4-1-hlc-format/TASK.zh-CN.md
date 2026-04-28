# 理解并实现混合逻辑时钟的格式

英文标题：Understand and Implement HLC Format
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-1-hlc-format>

课程：2. 标识符：分布式唯一 ID
任务序号：16
短标题：混合逻辑时钟格式
难度：高级
子主题：Hybrid Logical Clocks (HLC)

## 中文导读

混合逻辑时钟（HLC）是 CockroachDB 和 Spanner 等数据库使用的时钟方案，它将物理时间和逻辑计数器结合在一起，既保留了物理时间的直观性，又具备逻辑时钟的单调递增特性。本题要求你实现混合逻辑时钟的基本格式和本地事件的更新规则。

## 题目说明

混合逻辑时钟（HLC，Hybrid Logical Clock）被 CockroachDB 和 Spanner 等分布式数据库广泛使用。它将物理时间与逻辑计数器组合在一起，格式为 `(physical_ms, logical_counter)`。

可以这样理解：物理时间就像墙上的挂钟，告诉你"大概几点了"；逻辑计数器就像同一秒内的流水号，用来区分同一毫秒内发生的多个事件。两者结合，既能关联现实时间，又能保证严格递增。

当**本地事件发生**或**发送消息**时，更新规则如下：
1. 获取当前物理时间 `pt`
2. 如果 `pt > hlc.pt`：说明物理时间前进了，设置 `hlc.pt = pt`，`hlc.lc = 0`（重置逻辑计数器）
3. 否则：物理时间没有前进（可能在同一毫秒内），保持 `hlc.pt` 不变，逻辑计数器加 1（`hlc.lc += 1`）

实现 `hlc_tick`（触发一次本地事件）和 `hlc_get`（获取当前时钟状态）两个处理器：

```json
请求:  {"type": "hlc_tick", "msg_id": 1}
响应: {"type": "hlc_tick_ok", "in_reply_to": 1, "pt": 1234567, "lc": 0}
```

```json
请求:  {"type": "hlc_get", "msg_id": 2}
响应: {"type": "hlc_get_ok", "in_reply_to": 2, "pt": 1234567, "lc": 0}
```

## 涉及概念

- `HLC`
- `hybrid clock`
- `physical time`
- `logical counter`

## 实现提示

- 混合逻辑时钟是一个二元组：（物理时间毫秒数，逻辑计数器）
- 物理时间来自系统时钟
- 逻辑计数器用于区分同一毫秒内发生的多个事件
- 混合逻辑时钟始终向前推进，即使系统时钟发生了回退也不会倒退
- 发送事件时：如果物理时间大于当前记录的最大物理时间，重置计数器；否则递增计数器

## 测试用例

### 1. 触发事件后返回物理时间和逻辑计数器

`hlc_tick_ok` 响应应包含 pt > 0 且 lc = 0（第一次触发会获取最新的物理时间）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 获取初始的零状态

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_get","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_get_ok", "pt": 0, "lc": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Hybrid Logical Clocks (Kulkarni et al.)](https://cse.buffalo.edu/tech-reports/2014-04.pdf)：混合逻辑时钟的原始论文，由 Kulkarni、Demirbas 等人撰写

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
