# 实现带溢出处理的序列计数器

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-3-sequence-counter>

课程：2. 标识符：分布式唯一 ID
任务序号：8
短标题：序列计数器
难度：进阶
子主题：雪花 ID（Twitter 的方案）

## 中文导读

雪花 ID 中的 12 位序列号决定了每毫秒最多能生成 4096 个 ID。如果流量突增超过了这个上限怎么办？这道题让你实现序列计数器，并优雅地处理溢出：当序列号用完时，等到下一毫秒再继续生成。

## 题目说明

在同一毫秒内，每个雪花节点最多可以生成 4096 个唯一 ID（12 位序列计数器）。当流量突增超过这个限制时，生成器必须优雅地处理**序列溢出**。

你需要实现序列计数器的以下功能：

1. 每进入一个新的毫秒，将序列号重置为 0
2. 在同一毫秒内，每生成一个 ID，序列号加 1
3. 当序列号溢出（大于 4095）时，忙等待（Spin Wait）直到下一毫秒，然后重置
4. 跟踪每毫秒达到的最大序列号，用于吞吐量分析

实现 `generate_batch` 消息处理器，一次性生成 N 个 ID：

```json
Request:  {"type": "generate_batch", "msg_id": 1, "count": 10}
Response: {"type": "generate_batch_ok", "in_reply_to": 1, "ids": [1, 2, 3, ...], "max_sequence": 9}
```

所有生成的 ID 必须唯一且单调递增。

## 涉及概念

- `sequence number`
- `overflow handling`
- `spin wait`
- `throughput limits`

## 实现提示

- 序列计数器在同一毫秒内每生成一个 ID 就递增一次
- 进入新的毫秒时将序列号重置为 0
- 如果序列号溢出（超过 4095），等待到下一个毫秒
- 这里使用忙等待是可以接受的，因为毫秒级的切换非常快
- 记录达到的最大序列号，用于吞吐量分析

## 测试用例

### 1. 单次生成正常工作

验证说明：应产生一个包含数值型 `id` 的 `generate_ok` 响应。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 批量生成 5 个唯一 ID

验证说明：响应类型应为 `generate_batch_ok`，包含长度为 5 的 `ids` 数组（所有 ID 唯一），以及 `max_sequence` 字段。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate_batch","msg_id":2,"count":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Globally Unique ID Generation](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c)：Instagram 工程团队关于大规模 ID 生成的实践分享

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
