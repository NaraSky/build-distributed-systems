# 构建 Stream Processing Pipeline

英文标题：Build Stream Processing Pipeline
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-4-streaming>

课程：10. 高级主题
任务序号：4
短标题：Streaming
难度：intermediate
子主题：高级 Paradigms

## 中文导读

本题要求你完成 `构建 Stream Processing Pipeline`。

重点关注：`streaming`、`windowing`、`exactly-once`。

建议先按提示逐步实现：Tumbling vs sliding windows。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build stream processor，包含windowing. Support tumbling和sliding windows，包含event-time processing.

## 概念说明

### Stream Processing

Unlike batch, stream processes data continuously. Windows aggregate over time. Watermarks handle late data in event-time processing.

## 涉及概念

- `streaming`
- `windowing`
- `exactly-once`

## 实现提示

- Tumbling vs sliding windows
-处理late arrivals
- Watermarks用于event-time

## 测试用例

### 1. 添加 event to window

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"stream_event","msg_id":2,"event":{"data":"click","value":1},"timestamp":5,"window_size":10}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"stream_event_ok","in_reply_to":2,"msg_id":1,"window_key":0,"window_events":1}}
```

## 参考资料

- [Streaming 101](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-101)：Streaming concepts

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
