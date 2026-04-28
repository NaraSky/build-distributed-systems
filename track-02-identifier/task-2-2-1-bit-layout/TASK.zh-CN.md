# 实现 Snowflake ID Bit Layout

英文标题：Implement Snowflake ID Bit Layout
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-1-bit-layout>

课程：2. 标识符：分布式唯一 ID
任务序号：6
短标题：Bit Layout
难度：intermediate
子主题：Snowflake IDs (Twitter's Approach)

## 中文导读

本题要求你完成 `实现 Snowflake ID Bit Layout`。

重点关注：`bit manipulation`、`Snowflake ID`、`bit layout`、`scalability`。

建议先按提示逐步实现：Use left shift (<<) to position each component in the 64-bit integer。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Twitter's Snowflake generates unique, roughly-sorted 64-bit IDs without coordination. The layout is:

```
| 1 bit unused | 41 bits timestamp | 10 bits machine ID | 12 bits sequence |
|     0        |   ms since epoch  |    0-1023          |    0-4095        |
```

Your task is to implement functions that:

1. **Compose** a Snowflake ID from its three components (timestamp_ms, machine_id, sequence)
2. **Decompose** a Snowflake ID back into its components
3.处理the Maelstrom `generate` workload使用Snowflake IDs

Implement a `generate` 消息 handler:
```JSON
请求:  {"type": "generate", "msg_id": 1}
响应: {"type": "generate_ok", "in_reply_to": 1, "id": 7041429939834880}
```

And a `decompose` handler用于debugging:
```JSON
请求:  {"type": "decompose", "msg_id": 2, "id": 7041429939834880}
响应: {"type": "decompose_ok", "in_reply_to": 2, "timestamp_ms": 1678886400000, "machine_id": 1, "sequence": 0}
```

## 涉及概念

- `bit manipulation`
- `Snowflake ID`
- `bit layout`
- `scalability`

## 实现提示

- Use left shift (<<) to position each component in the 64-bit integer
- Timestamp goes in the top 41 bits, machine ID in the next 10, sequence in the bottom 12
- Use bitwise OR (|) to combine the components
- To extract components, use right shift (>>)和bitwise AND (&)，包含masks
- Max IDs per ms per 节点 = 2^12 = 4096

## 测试用例

### 1. 初始化和generate produces an ID

The second line should be a generate_ok，包含a numeric id field. Exact value varies by timestamp.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Two sequential generates produce different IDs

Two generate_ok responses，包含different id values. The second ID should be greater than or equal to the first.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Twitter Snowflake (Original Announcement)](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake)：Twitter engineering blog post introducing Snowflake ID generation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
