# 实现 Sequence 计数器，包含Overflow处理

英文标题：Implement Sequence Counter，包含Overflow处理
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-3-sequence-counter>

课程：2. 标识符：分布式唯一 ID
任务序号：8
短标题：Sequence 计数器
难度：intermediate
子主题：Snowflake IDs (Twitter's Approach)

## 中文导读

本题要求你完成 `实现 Sequence 计数器，包含Overflow处理`。

重点关注：`sequence number`、`overflow handling`、`spin wait`、`throughput limits`。

建议先按提示逐步实现：The sequence 计数器 increments用于each ID generated in the same millisecond。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Within a single millisecond, each Snowflake 节点 can generate up to 4096 unique IDs (12-bit sequence 计数器). When traffic bursts exceed this limit, the generator must handle **sequence overflow** gracefully.

Your task is to implement the sequence 计数器:

1. Initialize to 0 at the start of each new millisecond
2. Increment by 1用于each ID generated in the same millisecond
3. On overflow (sequence > 4095), spin-wait until the next millisecond, then reset
4. Track maximum sequence reached per millisecond用于throughput analysis

Implement a `generate_batch` 消息 that generates N IDs at once:

```JSON
请求:  {"type": "generate_batch", "msg_id": 1, "count": 10}
响应: {"type": "generate_batch_ok", "in_reply_to": 1, "ids": [1, 2, 3, ...], "max_sequence": 9}
```

All generated IDs must be unique和monotonically increasing.

## 涉及概念

- `sequence number`
- `overflow handling`
- `spin wait`
- `throughput limits`

## 实现提示

- The sequence 计数器 increments用于each ID generated in the same millisecond
- Reset the sequence to 0 when moving to a new millisecond
- If the sequence overflows (>4095), wait until the next millisecond
- Spin-waiting is acceptable here since millisecond transitions are fast
- Track the max sequence reached用于throughput analysis

## 测试用例

### 1. Single generate works

Should produce a generate_ok，包含a numeric id.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Batch of 5 produces 5 唯一 IDs

响应 should have type generate_batch_ok，包含ids array of length 5, all unique,和a max_sequence field.

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

- [Globally Unique ID Generation](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c)：Instagram engineering on ID generation at scale

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
