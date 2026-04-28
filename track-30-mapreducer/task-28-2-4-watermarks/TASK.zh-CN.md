# 使用水位线处理乱序事件

英文标题：Handle Out-of-Order Events with Watermarks
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-4-watermarks>

课程：30. MapReducer：批处理与流处理
任务序号：9
短标题：水位线
难度：高级
子主题：Stream Processing

## 中文导读

本题要求你实现水位线（Watermark）机制来处理乱序事件。在分布式流处理中，事件不一定按发生的先后顺序到达。比如 10:00:00 发生的点击事件，可能因为网络延迟，反而在 10:00:05 的事件之后才到达。水位线告诉系统"在这个时间点之前的事件大概率都已经到了"，从而决定何时可以安全地关闭窗口。迟到太多的事件则直接丢弃。

## 题目说明

分布式流中的事件并不总是按照发生顺序到达。由于网络延迟，10:00:00 的点击事件可能在 10:00:05 的事件之后才到达。如果不处理这种情况，10:00:00 的事件会因为窗口已经关闭而被丢弃。

**水位线（Watermark）** 解决了这个问题：水位线代表处理器认为"在此时间点之前的所有数据都已到达"的事件时间点。随着更新的事件到达，水位线不断推进。只有当水位线超过窗口的结束边界时，窗口才会关闭。

```
允许延迟时间 = 30秒

事件到达情况:
  10:00:10  -> 水位线 = 10:00:10 - 30秒 = 09:59:40
  10:00:30  -> 水位线 = 10:00:30 - 30秒 = 10:00:00
  10:00:00  -> 迟到（事件时间 < 水位线），但窗口仍然开放 -> 接受
  10:01:00  -> 水位线 = 10:01:00 - 30秒 = 10:00:30
```

你的节点需要处理两种消息类型：

```json
// 根据已观察到的最大时间戳计算水位线
{ "type": "watermark", "msg_id": 1,
  "max_timestamp": "2024-01-15T10:00:00Z",
  "allowed_lateness_ms": 30000 }
-> { "type": "watermark", "in_reply_to": 1,
    "watermark": "2024-01-15T09:59:30Z" }

// 处理一个事件 -- 判断它是迟到还是准时
{ "type": "process", "msg_id": 2,
  "event": {"id": 1},
  "event_time": "2024-01-15T10:00:00Z",
  "watermark":  "2024-01-15T10:00:30Z" }
-> { "type": "late_event", "in_reply_to": 2,
    "event_id": 1, "handled": "dropped" }
```

当事件时间小于水位线时，该事件被视为迟到事件。迟到事件会被丢弃。

## 概念说明

水位线可以类比为火车站的发车时间。假设火车（窗口关闭）定于 10:00 发车，但允许乘客迟到 30 秒。那么水位线就是"当前时间减去 30 秒"。如果现在是 10:00:30，水位线就推进到 10:00:00，意味着 10:00:00 之前的乘客已经不能上车了（窗口关闭）。10:00:00 之后到的乘客还有机会赶上。

## 涉及概念

- `watermarks`
- `out-of-order events`
- `event time`
- `allowed lateness`
- `late event handling`

## 实现提示

- 水位线 = 迄今观察到的最大事件时间戳 - 允许延迟时间
- 如果事件时间小于当前水位线，则该事件为迟到事件
- 当水位线超过窗口结束时间时，窗口关闭
- 落在仍然开放的窗口内的迟到事件可以被接受；其他的则被丢弃
- 水位线只会向前推进，不会回退

## 测试用例

### 1. 生成水位线

水位线 = 最大时间戳 - 允许延迟时间（提前 30 秒）。

输入：

```json
{"src":"generator","dest":"processor","body":{"type":"watermark","msg_id":1,"max_timestamp":"2024-01-15T10:00:00Z","allowed_lateness_ms":30000}}
```

期望输出：

```text
{"type": "watermark", "in_reply_to": 1, "watermark": "2024-01-15T09:59:30Z"}
```

### 2. 处理迟到事件

事件时间 10:00:00 小于水位线 10:00:30，因此事件迟到并被丢弃。

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"event":{"id":1},"event_time":"2024-01-15T10:00:00Z","watermark":"2024-01-15T10:00:30Z"}}
```

期望输出：

```text
{"type": "late_event", "in_reply_to": 1, "event_id": 1, "handled": "dropped"}
```

## 参考资料

- [Watermarks in Stream Processing](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-102)：水位线如何实现正确的乱序事件处理

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
