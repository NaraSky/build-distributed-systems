# 实现 Timestamp Component，包含Custom Epoch

英文标题：Implement Timestamp Component，包含Custom Epoch
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-2-timestamp-component>

课程：2. 标识符：分布式唯一 ID
任务序号：7
短标题：Custom Epoch
难度：intermediate
子主题：Snowflake IDs (Twitter's Approach)

## 中文导读

本题要求你完成 `实现 Timestamp Component，包含Custom Epoch`。

重点关注：`timestamp`、`epoch`、`time representation`、`overflow planning`。

建议先按提示逐步实现：A custom epoch starting in 2024 gives you ~69 years before 41 bits overflow。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The timestamp component of a Snowflake ID uses 41 bits to represent milliseconds since a **custom epoch**.使用Unix epoch (1970-01-01) wastes over 50 years of timestamp space. A custom epoch starting in 2024 gives the system ~69 years of IDs.

Your task is to:

1. Implement timestamp generation relative to a custom epoch (2024-01-01 00:00:00 UTC)
2. Validate that the timestamp fits within 41 bits
3. Implement a `time_info` 消息 that reports the current timestamp state

```JSON
请求:  {"type": "time_info", "msg_id": 1}
响应: {"type": "time_info_ok", "in_reply_to": 1, 
           "current_ms": 1234567, 
           "custom_epoch_ms": 1704067200000,
           "max_timestamp_ms": 2199023255551,
           "years_remaining": 69}
```

Also implement `generate` that uses the custom epoch用于timestamps,和verify IDs are monotonically increasing:
```JSON
请求:  {"type": "generate", "msg_id": 1}
响应: {"type": "generate_ok", "in_reply_to": 1, "id": 1234567890}
```

## 涉及概念

- `timestamp`
- `epoch`
- `time representation`
- `overflow planning`

## 实现提示

- A custom epoch starting in 2024 gives you ~69 years before 41 bits overflow
- Unix epoch (1970) would waste 54 years of timestamp space
- Use time.time() * 1000 to get current timestamp in milliseconds
- Subtract the custom epoch to get relative milliseconds
- Check that the timestamp fits in 41 bits before composing the ID

## 测试用例

### 1. Generate produces a numeric ID

The generate_ok 响应 should contain a numeric id field greater than 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Time info returns epoch和years remaining

响应 should contain custom_epoch_ms=1704067200000, max_timestamp_ms=2199023255551, current_ms > 0,和years_remaining > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"time_info","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Time, Clocks,和the Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)：Lamport paper on logical clocks和event ordering in 分布式系统

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
