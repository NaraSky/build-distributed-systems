# Multi-Node Snowflake ID Verification

英文标题：Multi-Node Snowflake ID Verification
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-5-multi-node>

课程：2. 标识符：分布式唯一 ID
任务序号：10
短标题：Multi-Node IDs
难度：advanced
子主题：Snowflake IDs (Twitter's Approach)

## 中文导读

本题要求你完成 `Multi-Node Snowflake ID Verification`。

重点关注：`multi-node coordination`、`uniqueness verification`、`monotonicity`、`ID distribution`。

建议先按提示逐步实现：Each 节点 uses its own machine_id extracted from the node_id。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Snowflake IDs derive their uniqueness from the machine_id component. With 10 bits, you can have 1024 unique machines generating IDs without any coordination.

Your task is to verify uniqueness和ordering across multiple 节点:

1. Extract machine_id from Maelstrom node_id (e.g., "n3" -> machine_id 3)
2. Generate IDs和verify they are unique within a 节点
3. Implement a `verify_ids` handler that checks a list of IDs用于uniqueness和ordering

```JSON
请求:  {"type": "verify_ids", "msg_id": 1, "ids": [100, 200, 300, 200]}
响应: {"type": "verify_ids_ok", "in_reply_to": 1, "count": 4, "unique": 3, "is_sorted": false, "duplicates": [200]}
```

## 涉及概念

- `multi-node coordination`
- `uniqueness verification`
- `monotonicity`
- `ID distribution`

## 实现提示

- Each 节点 uses its own machine_id extracted from the node_id
- IDs from different 节点 are unique because the machine_id bits differ
- Within a single 节点, IDs must be monotonically increasing
- Across 节点, IDs are only roughly sorted due to 时钟 differences
- Use the decompose function to verify machine_id extraction

## 测试用例

### 1. Verify sorted 唯一 IDs

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"verify_ids","msg_id":2,"ids":[10,20,30]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "verify_ids_ok", "count": 3, "unique": 3, "is_sorted": true, "duplicates": [], "in_reply_to": 2, "msg_id": 1}}
```

### 2. Detect duplicates in ID list

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"verify_ids","msg_id":2,"ids":[10,20,10,30]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "verify_ids_ok", "count": 4, "unique": 3, "is_sorted": false, "duplicates": [10], "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Unique ID Generation at Scale](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake)：Twitter Snowflake announcement blog post

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
