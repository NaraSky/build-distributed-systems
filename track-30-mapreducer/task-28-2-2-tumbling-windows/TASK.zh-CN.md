# 实现翻滚窗口

英文标题：Implement Tumbling Windows
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-2-tumbling-windows>

课程：30. MapReducer：批处理与流处理
任务序号：7
短标题：翻滚窗口
难度：进阶
子主题：Stream Processing

## 中文导读

本题要求你实现流处理中的翻滚窗口（Tumbling Window）。面对无限的事件流，我们经常需要按固定时间段来统计数据，比如"每分钟收到了多少条消息"。翻滚窗口就是把时间轴切成一段一段等长的、互不重叠的区间，每个事件恰好落入其中一个窗口。这是流处理中最基础的时间窗口模型。

## 题目说明

翻滚窗口（Tumbling Window）将无限的事件流划分为固定大小的、**互不重叠**的时间桶。每个事件恰好属于一个窗口。当窗口时间结束时，输出该窗口的聚合结果并开始一个全新的窗口。

```
事件:    e1(10:00:10)  e2(10:00:40)  e3(10:01:15)  e4(10:01:50)
窗口:    [---- 10:00 - 10:01 ----]   [---- 10:01 - 10:02 ----]
         e1, e2  ->  count=2          e3, e4  ->  count=2
```

你的节点需要处理以下消息类型：

```json
// 将单个事件分配到它所属的窗口（window_size_ms = 60000 表示 1 分钟的窗口）
{ "type": "assign", "msg_id": 1,
  "events": [{"id":1,"timestamp":"2024-01-15T10:00:10Z"}],
  "window_size_ms": 60000 }
-> { "type": "assigned", "in_reply_to": 1,
    "window_id": "window-1705305600000",
    "window_start": "2024-01-15T10:00:00Z",
    "window_end":   "2024-01-15T10:01:00Z" }

// 处理一组事件并返回各窗口的聚合结果
{ "type": "process_window", "msg_id": 2,
  "events": [
    {"id":1,"timestamp":"2024-01-15T10:00:10Z"},
    {"id":2,"timestamp":"2024-01-15T10:00:40Z"},
    {"id":3,"timestamp":"2024-01-15T10:01:15Z"}
  ],
  "window_size_ms": 60000 }
-> { "type": "window_result", "in_reply_to": 2,
    "windows": [
      {"window_id":"window-1705305600000","count":2,"events":[1,2]},
      {"window_id":"window-1705305660000","count":1,"events":[3]}
    ]}
```

窗口标识的计算公式为：`floor(timestamp_ms / window_size_ms) * window_size_ms`

## 概念说明

翻滚窗口就像一条传送带上等距排列的篮子：每个篮子代表一个固定的时间区间。事件像球一样落到传送带上，每个球根据它的时间戳恰好落入一个篮子。篮子之间没有重叠，也没有间隙。每个篮子装满后（窗口结束），就统计里面有多少球，然后下一个空篮子接着装。

## 涉及概念

- `tumbling windows`
- `time-based windows`
- `window aggregation`
- `non-overlapping windows`
- `event time`

## 实现提示

- 窗口标识 = floor(事件时间戳毫秒值 / 窗口大小毫秒值) * 窗口大小毫秒值
- 每个事件恰好属于一个窗口，窗口之间不重叠
- 窗口结束时间 = 窗口开始时间 + 窗口大小
- 按窗口标识聚合事件：维护每个窗口的计数和事件列表
- 关闭操作输出某个窗口的结果并将其从活跃状态中移除

## 测试用例

### 1. 将事件分配到窗口

应将事件正确分配到 1 分钟的翻滚窗口中。

输入：

```json
{"src":"stream","dest":"windower","body":{"type":"assign","msg_id":1,"events":[{"id":1,"timestamp":"2024-01-15T10:00:10Z"}],"window_size_ms":60000}}
```

期望输出：

```text
{"type": "assigned", "in_reply_to": 1, "window_id": "window-1705305600000", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:01:00Z"}
```

### 2. 处理多个窗口

应将事件分组到两个独立的 1 分钟窗口中。

输入：

```json
{"src":"stream","dest":"windower","body":{"type":"process_window","msg_id":1,"events":[{"id":1,"timestamp":"2024-01-15T10:00:10Z"},{"id":2,"timestamp":"2024-01-15T10:00:40Z"},{"id":3,"timestamp":"2024-01-15T10:01:15Z"}],"window_size_ms":60000}}
```

期望输出：

```text
{"type": "window_result", "in_reply_to": 1, "windows": [{"window_id": "window-1705305600000", "count": 2, "events": [1, 2]}, {"window_id": "window-1705305660000", "count": 1, "events": [3]}]}
```

## 参考资料

- [Streaming 102 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-102)：介绍包括翻滚窗口在内的各种窗口模型

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
