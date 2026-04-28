# 实现 Sliding Windows

英文标题：Implement Sliding Windows
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-3-sliding-windows>

课程：30. MapReducer：批处理与流处理
任务序号：8
短标题：Sliding Windows
难度：advanced
子主题：Stream Processing

## 中文导读

本题要求你完成 `实现 Sliding Windows`。

重点关注：`sliding windows`、`overlapping windows`、`window size`、`slide interval`、`moving average`。

建议先按提示逐步实现：An event at time T belongs to every window whose [start, end) contains T。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Tumbling windows are non-overlapping — an event belongs to exactly one window. Sliding windows **overlap**: each event belongs to multiple windows, enabling smooth rolling aggregations like "average latency over the last 5 minutes, updated every minute".

```
window_size=5min, slide=1min

Events at 10:02: ---e1---

Windows containing e1:
  [10:00 - 10:05]  <- window starting at 10:00
  [10:01 - 10:06]  <- window starting at 10:01
  [10:02 - 10:07]  <- window starting at 10:02
```

Your 节点 handles two 消息 types:

```JSON
// Assign one event to all sliding windows it belongs to
{ "type": "assign", "msg_id": 1,
  "event_timestamp": "2024-01-15T10:02:00Z",
  "current_time":    "2024-01-15T10:03:00Z",
  "window_size_ms":  300000,
  "slide_ms":        60000 }
→ { "type": "assigned", "in_reply_to": 1,
    "windows": [
      {"window_id": "...", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:05:00Z"},
      {"window_id": "...", "window_start": "2024-01-15T10:01:00Z", "window_end": "2024-01-15T10:06:00Z"},
      {"window_id": "...", "window_start": "2024-01-15T10:02:00Z", "window_end": "2024-01-15T10:07:00Z"}
    ]}

// List all windows active at the given time
{ "type": "active_windows", "msg_id": 2,
  "current_time": "2024-01-15T10:03:00Z",
  "window_size_ms": 300000,
  "slide_ms": 60000 }
→ { "type": "active_windows_result", "in_reply_to": 2, "count": 5 }
```

The key difference from tumbling windows: `window_size_ms / slide_ms` windows are active at any point in time.

## 涉及概念

- `sliding windows`
- `overlapping windows`
- `window size`
- `slide interval`
- `moving average`

## 实现提示

- An event at time T belongs to every window whose [start, end) contains T
- Window starts: all multiples of slide_ms from (T - window_size_ms) up to T
- Number of windows per event = window_size_ms / slide_ms
- For active_windows, list all windows that overlap，包含current_time
- Moving average: sum event values across the window, divide by count

## 测试用例

### 1. Assign to sliding windows

Event at 10:02 should belong to 3 overlapping 5-min windows.

输入：

```json
{"src":"stream","dest":"windower","body":{"type":"assign","msg_id":1,"event_timestamp":"2024-01-15T10:02:00Z","current_time":"2024-01-15T10:03:00Z","window_size_ms":300000,"slide_ms":60000}}
```

期望输出：

```text
{"type": "assigned", "in_reply_to": 1, "windows": [{"window_id": "window-1705305600000-1705307400000", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:05:00Z"}, {"window_id": "window-1705305660000-1705307460000", "window_start": "2024-01-15T10:01:00Z", "window_end": "2024-01-15T10:06:00Z"}, {"window_id": "window-1705305720000-1705307520000", "window_start": "2024-01-15T10:02:00Z", "window_end": "2024-01-15T10:07:00Z"}]}
```

### 2. Count active windows

window_size/slide = 300000/60000 = 5 active windows at any moment.

输入：

```json
{"src":"stream","dest":"windower","body":{"type":"active_windows","msg_id":1,"current_time":"2024-01-15T10:03:00Z","window_size_ms":300000,"slide_ms":60000}}
```

期望输出：

```text
{"type": "active_windows_result", "in_reply_to": 1, "count": 5}
```

## 参考资料

- [Streaming 102 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-102)：Windowing models: tumbling, sliding,和session windows

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
