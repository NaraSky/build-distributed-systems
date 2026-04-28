# 实现模拟版 TrueTime 接口

英文标题：Implement Mock TrueTime API
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-4-truetime-mock>

课程：16. 时间守卫：逻辑时钟
任务序号：4
短标题：TrueTime 模拟
难度：高级
子主题：物理时间及其缺陷

## 中文导读

这道题让你实现一个模拟版的 TrueTime 接口。普通的时钟返回的是一个时间点，而 TrueTime 返回的是一个时间区间——它诚实地告诉你"真实时间在这个范围内"。这是 Google Spanner 数据库的核心设计思想：与其假装时钟是精确的，不如明确承认不确定性（Uncertainty），并在此基础上构建正确的系统。

## 题目说明

Google Spanner 的 TrueTime 接口不返回一个精确的时间点，而是返回一个时间区间：`now() -> [earliest, latest]`，保证真实时间一定落在这个区间内。

你需要实现一个可配置不确定性窗口的模拟版 TrueTime：
```json
Request:  {"type": "truetime_now", "msg_id": 1}
Response: {"type": "truetime_now_ok", "in_reply_to": 1, "earliest": 1234560, "latest": 1234574, "uncertainty_ms": 7}

Request:  {"type": "set_uncertainty", "msg_id": 2, "uncertainty_ms": 10}
Response: {"type": "set_uncertainty_ok", "in_reply_to": 2}
```

## 涉及概念

- `TrueTime`
- `Google Spanner`
- `uncertainty interval`
- `bounded error`

## 实现提示

- TrueTime 返回 `[earliest, latest]` 区间，而不是单个时间戳
- 在配备 GPS 和原子钟的环境下，不确定性窗口通常约为 7 毫秒
- 计算方式为：`earliest = now - uncertainty`，`latest = now + uncertainty`
- 任何发生在真实时间 T 的事件，其 T 值一定在 `[earliest, latest]` 区间内
- 这就是 Google Spanner 实现外部一致性（External Consistency）的基础

## 测试用例

### 1. 获取 TrueTime 时间区间

返回的 `truetime_now_ok` 中应满足 `earliest < latest` 且 `uncertainty_ms=7`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"truetime_now","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 设置不确定性窗口

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

- [Spanner: Google Globally-Distributed Database](https://research.google/pubs/pub39966/)：描述 TrueTime 的 Google Spanner 原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
