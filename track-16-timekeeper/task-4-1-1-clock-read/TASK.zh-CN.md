# 读取系统时钟并检测时间回跳

英文标题：Read System Clock and Detect Backward Jumps
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-1-clock-read>

课程：16. 时间守卫：逻辑时钟
任务序号：1
短标题：时钟读取
难度：进阶
子主题：物理时间及其缺陷

## 中文导读

这道题要求你反复读取系统时钟，并检测其中是否出现了"时间回跳"——也就是后一次读到的时间反而比前一次更早。这种现象在分布式系统中经常发生，因为 NTP（Network Time Protocol）同步时会调整系统时钟，可能导致时间突然往回跳。理解这一问题，是掌握分布式系统中"时间不可靠"这一核心概念的第一步。

## 题目说明

系统时钟（System Clock）并不像我们直觉中那样永远向前走。当 NTP 服务对系统时钟进行校正时，时间可能会突然往回跳。你的任务是：反复读取系统时钟，检测并统计这种回跳现象。

实现一个 `clock_sample` 消息处理器，连续读取时钟 N 次，并返回统计信息：
```json
Request:  {"type": "clock_sample", "msg_id": 1, "count": 100, "offset_ms": 0}
Response: {"type": "clock_sample_ok", "in_reply_to": 1, "samples": 100, "backward_jumps": 0, "max_delta_us": 15, "min_delta_us": 1}
```

同时实现 `simulate_ntp` 消息处理器，用于模拟注入一个回跳偏移量：
```json
Request:  {"type": "simulate_ntp", "msg_id": 2, "offset_ms": -50}
Response: {"type": "simulate_ntp_ok", "in_reply_to": 2}
```

## 涉及概念

- `system clock`
- `clock monotonicity`
- `NTP`
- `backward jump`

## 实现提示

- 使用墙上时钟（Wall Clock）获取当前时间，使用单调时钟（Monotonic Clock）获取不会回跳的时间
- 比较相邻两次读数，如果后一次比前一次小，就说明发生了回跳
- NTP 校正可能导致墙上时钟向后跳变
- 记录相邻读数之间的最小和最大时间差
- 将读数存储在缓冲区中以便分析

## 测试用例

### 1. 读取时钟并返回统计信息

返回的 `clock_sample_ok` 中应包含 `samples=10` 且 `backward_jumps=0`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"clock_sample","msg_id":2,"count":10}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 模拟 NTP 校正正常响应

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

- [Falsehoods Programmers Believe About Time](https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time)：程序员关于时间的常见误解

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
