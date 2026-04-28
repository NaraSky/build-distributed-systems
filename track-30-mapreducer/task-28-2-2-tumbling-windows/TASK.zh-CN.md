# 实现 Tumbling Windows

英文标题：Implement Tumbling Windows
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-2-tumbling-windows>

课程：30. MapReducer：批处理与流处理
任务序号：7
短标题：Tumbling Windows
难度：intermediate
子主题：Stream Processing

## 中文导读

本题要求你完成 `实现 Tumbling Windows`。

重点关注：`tumbling windows`、`time-based windows`、`window aggregation`、`non-overlapping windows`、`event time`。

建议先按提示逐步实现：Window ID = floor(event_timestamp_ms / window_size_ms) * window_size_ms。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Tumbling windows divide an infinite stream into fixed-size, **non-overlapping** time buckets. Each event belongs to exactly one window. When the window period ends, you emit the aggregate和start a fresh window.

```
Events:  e1(10:00:10)  e2(10:00:40)  e3(10:01:15)  e4(10:01:50)
Windows: [---- 10:00 - 10:01 ----]   [---- 10:01 - 10:02 ----]
         e1, e2  →  count=2           e3, e4  →  count=2
```

Your 节点 handles three 消息 types:

```JSON
// Assign a single event to its window (window_size_ms = 60000 → 1-minute windows)
{ "type": "assign", "msg_id": 1,
  "events": [{"id":1,"timestamp":"2024-01-15T10:00:10Z"}],
  "window_size_ms": 60000 }
→ { "type": "assigned", "in_reply_to": 1,
    "window_id": "window-1705305600000",
    "window_start": "2024-01-15T10:00:00Z",
    "window_end":   "2024-01-15T10:01:00Z" }

// Process a stream of events和return window aggregates
{ "type": "process_window", "msg_id": 2,
  "events": [
    {"id":1,"timestamp":"2024-01-15T10:00:10Z"},
    {"id":2,"timestamp":"2024-01-15T10:00:40Z"},
    {"id":3,"timestamp":"2024-01-15T10:01:15Z"}
  ],
  "window_size_ms": 60000 }
→ { "type": "window_result", "in_reply_to": 2,
    "windows": [
      {"window_id":"window-1705305600000","count":2,"events":[1,2]},
      {"window_id":"window-1705305660000","count":1,"events":[3]}
    ]}
```

Window ID formula: `floor(timestamp_ms / window_size_ms) * window_size_ms`

## 涉及概念

- `tumbling windows`
- `time-based windows`
- `window aggregation`
- `non-overlapping windows`
- `event time`

## 实现提示

- Window ID = floor(event_timestamp_ms / window_size_ms) * window_size_ms
- Each event belongs to exactly one window — windows never overlap
- Window end = window_start + window_size_ms
- Aggregate events per window_id: keep a count和list of events
- close emits the result用于a window和removes it from active state

## 测试用例

### 1. Assign events to windows

Should assign event to correct 1-minute tumbling window.

输入：

```json
{"src":"stream","dest":"windower","body":{"type":"assign","msg_id":1,"events":[{"id":1,"timestamp":"2024-01-15T10:00:10Z"}],"window_size_ms":60000}}
```

期望输出：

```text
{"type": "assigned", "in_reply_to": 1, "window_id": "window-1705305600000", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:01:00Z"}
```

### 2. Process multiple windows

Should group events into two separate 1-minute windows.

输入：

```json
{"src":"stream","dest":"windower","body":{"type":"process_window","msg_id":1,"events":[{"id":1,"timestamp":"2024-01-15T10:00:10Z"},{"id":2,"timestamp":"2024-01-15T10:00:40Z"},{"id":3,"timestamp":"2024-01-15T10:01:15Z"}],"window_size_ms":60000}}
```

期望输出：

```text
{"type": "window_result", "in_reply_to": 1, "windows": [{"window_id": "window-1705305600000", "count": 2, "events": [1, 2]}, {"window_id": "window-1705305660000", "count": 1, "events": [3]}]}
```

## 参考资料

- [Streaming 102 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-102)：Covers windowing models including tumbling windows

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
