# 构建流处理管道

英文标题：Build Stream Processing Pipeline
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-4-streaming>

课程：10. 高级主题
任务序号：4
短标题：Streaming
难度：进阶
子主题：高级范式

## 中文导读

本题要求你构建一个支持窗口（Window）功能的流处理器。与批处理一次处理全部数据不同，流处理对数据进行持续不断的实时处理。你需要实现滚动窗口和滑动窗口，以及基于事件时间的处理。这是理解实时数据处理系统（如 Flink、Kafka Streams）的基础。

## 题目说明

构建一个带窗口功能的流处理器。支持滚动窗口（Tumbling Window）和滑动窗口（Sliding Window），以及基于事件时间（Event-Time）的处理。

## 概念说明

### 流处理

与批处理不同，流处理对数据进行持续处理。窗口（Window）机制将一段时间内的事件聚合在一起。水位线（Watermark）用于在事件时间处理中应对迟到的数据。你可以把窗口想象成一个个时间段的"桶"，事件按时间落入对应的桶中，然后对每个桶里的事件进行统计。

## 涉及概念

- `streaming`
- `windowing`
- `exactly-once`

## 实现提示

- 区分滚动窗口和滑动窗口：滚动窗口不重叠，滑动窗口可以重叠
- 处理迟到的事件
- 使用水位线来判断事件时间的推进

## 测试用例

### 1. 将事件添加到窗口

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

- [Streaming 101](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-101)：流处理的核心概念

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
