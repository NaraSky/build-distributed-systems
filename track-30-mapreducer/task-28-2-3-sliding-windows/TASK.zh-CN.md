# 实现滑动窗口

英文标题：Implement Sliding Windows
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-3-sliding-windows>

课程：30. MapReducer：批处理与流处理
任务序号：8
短标题：滑动窗口
难度：高级
子主题：Stream Processing

## 中文导读

本题要求你实现流处理中的滑动窗口（Sliding Window）。与翻滚窗口不同，滑动窗口之间是可以重叠的，同一个事件可能同时属于多个窗口。这使得滑动窗口非常适合计算"最近 5 分钟的平均延迟，每分钟更新一次"这类平滑的滚动统计。理解滑动窗口是掌握流处理高级窗口模型的关键一步。

## 题目说明

翻滚窗口是互不重叠的，每个事件恰好属于一个窗口。滑动窗口（Sliding Window）则是**可重叠**的：每个事件同时属于多个窗口，从而实现平滑的滚动聚合，比如"最近 5 分钟的平均延迟，每分钟更新一次"。

```
窗口大小=5分钟, 滑动步长=1分钟

10:02 时刻的事件: ---e1---

包含 e1 的窗口:
  [10:00 - 10:05]  <- 从 10:00 开始的窗口
  [10:01 - 10:06]  <- 从 10:01 开始的窗口
  [10:02 - 10:07]  <- 从 10:02 开始的窗口
```

你的节点需要处理两种消息类型：

```json
// 将一个事件分配到它所属的所有滑动窗口
{ "type": "assign", "msg_id": 1,
  "event_timestamp": "2024-01-15T10:02:00Z",
  "current_time":    "2024-01-15T10:03:00Z",
  "window_size_ms":  300000,
  "slide_ms":        60000 }
-> { "type": "assigned", "in_reply_to": 1,
    "windows": [
      {"window_id": "...", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:05:00Z"},
      {"window_id": "...", "window_start": "2024-01-15T10:01:00Z", "window_end": "2024-01-15T10:06:00Z"},
      {"window_id": "...", "window_start": "2024-01-15T10:02:00Z", "window_end": "2024-01-15T10:07:00Z"}
    ]}

// 列出在给定时间点处于活跃状态的所有窗口
{ "type": "active_windows", "msg_id": 2,
  "current_time": "2024-01-15T10:03:00Z",
  "window_size_ms": 300000,
  "slide_ms": 60000 }
-> { "type": "active_windows_result", "in_reply_to": 2, "count": 5 }
```

与翻滚窗口的关键区别在于：在任意时间点，同时处于活跃状态的窗口数量等于 `window_size_ms / slide_ms`。

## 概念说明

如果说翻滚窗口像传送带上不重叠的篮子，那滑动窗口就像一组相互交叠的放大镜在时间轴上滑动。每隔一个滑动步长就有一个新窗口开始，但每个窗口的持续时间比滑动步长长得多，所以窗口之间是有重叠的。一个事件可以同时被多个"放大镜"看到。这样做的好处是统计结果更平滑，不会因为窗口边界的变化产生突变。

## 涉及概念

- `sliding windows`
- `overlapping windows`
- `window size`
- `slide interval`
- `moving average`

## 实现提示

- 时间 T 的事件属于每一个区间 [start, end) 包含 T 的窗口
- 窗口起始时间：从 (T - window_size_ms) 到 T 之间所有 slide_ms 的整数倍
- 每个事件所属的窗口数量 = window_size_ms / slide_ms
- 对于活跃窗口查询，列出所有与当前时间重叠的窗口
- 移动平均值：对窗口内的事件值求和，再除以事件数量

## 测试用例

### 1. 分配到滑动窗口

10:02 的事件应属于 3 个重叠的 5 分钟窗口。

输入：

```json
{"src":"stream","dest":"windower","body":{"type":"assign","msg_id":1,"event_timestamp":"2024-01-15T10:02:00Z","current_time":"2024-01-15T10:03:00Z","window_size_ms":300000,"slide_ms":60000}}
```

期望输出：

```text
{"type": "assigned", "in_reply_to": 1, "windows": [{"window_id": "window-1705305600000-1705307400000", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:05:00Z"}, {"window_id": "window-1705305660000-1705307460000", "window_start": "2024-01-15T10:01:00Z", "window_end": "2024-01-15T10:06:00Z"}, {"window_id": "window-1705305720000-1705307520000", "window_start": "2024-01-15T10:02:00Z", "window_end": "2024-01-15T10:07:00Z"}]}
```

### 2. 统计活跃窗口数量

窗口大小除以滑动步长 = 300000 / 60000 = 在任意时刻有 5 个活跃窗口。

输入：

```json
{"src":"stream","dest":"windower","body":{"type":"active_windows","msg_id":1,"current_time":"2024-01-15T10:03:00Z","window_size_ms":300000,"slide_ms":60000}}
```

期望输出：

```text
{"type": "active_windows_result", "in_reply_to": 1, "count": 5}
```

## 参考资料

- [Streaming 102 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-102)：介绍翻滚窗口、滑动窗口和会话窗口等窗口模型

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
