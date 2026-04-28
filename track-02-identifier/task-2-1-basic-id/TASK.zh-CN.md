# Generate 唯一 IDs使用Node ID和Timestamp

英文标题：Generate Unique IDs使用Node ID和Timestamp
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-1-basic-id>

课程：2. 标识符：分布式唯一 ID
任务序号：1
短标题：基础 ID Generation
难度：beginner
子主题：Why 唯一 IDs Are Hard

## 中文导读

本题要求你完成 `Generate 唯一 IDs使用Node ID和Timestamp`。

重点关注：`unique IDs`、`timestamps`、`node identity`。

建议先按提示逐步实现：Combine node_id，包含a timestamp用于basic uniqueness。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

分布式系统 need unique identifiers用于entities, events,和消息. Without a central authority, each 节点 must generate IDs independently while avoiding collisions.

Implement a generate workload handler that responds to generate requests，包含unique IDs:

```JSON
{
  "type": "generate",
  "msg_id": 1
}
```

Your 响应 should be:

```JSON
{
  "type": "generate_ok",
  "msg_id": 1,
  "in_reply_to": 1,
  "id": "unique-id-here"
}
```

For this first implementation, combine your node_id，包含a timestamp to create IDs. This provides uniqueness across 节点 (different node_ids)和over time (different timestamps).

## 概念说明

## Why 唯一 IDs Matter

Every **database record**, every **日志 entry**, every **消息** needs an identifier. In a distributed system, you cannot simply increment a 计数器 because multiple 节点 might generate the same number simultaneously.

### The Collision Problem

Consider a simple 计数器-based approach:

```text
Node A: counter = 1 → generates ID 1
Node B: counter = 1 → generates ID 1  // COLLISION!
```

Both 节点 generate the same ID because they have *no coordination*.

### Timestamp-Based IDs

Timestamps provide a natural ordering和uniqueness over time, but two 节点 might generate the same timestamp. By including the `node_id`, we guarantee uniqueness across 节点:

```text
ID = "{node_id}-{timestamp}"

Node A: "n1-1704067200000"
Node B: "n2-1704067200000"  // Different node_id = unique
```

### Remaining Challenge

However, a single 节点 might still generate duplicate IDs within the same millisecond. We'll address this in the next task.

## 涉及概念

- `unique IDs`
- `timestamps`
- `node identity`

## 实现提示

- Combine node_id，包含a timestamp用于basic uniqueness
- Consider使用millisecond precision
-格式: node_id-timestamp-sequence

## 测试用例

### 1. Generate single ID，包含初始化

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
```

## 参考资料

- [Unique ID Generation Challenge](https://fly.io/dist-sys/2/)：Fly.io gossip Glomers unique ID generation walkthrough

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
