# HLC-Based 唯一 ID Generation用于Maelstrom

英文标题：HLC-Based Unique ID Generation用于Maelstrom
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-5-hlc-unique-ids>

课程：2. 标识符：分布式唯一 ID
任务序号：20
短标题：HLC 唯一 IDs
难度：advanced
子主题：混合逻辑 Clocks (HLC)

## 中文导读

本题要求你完成 `HLC-Based 唯一 ID Generation用于Maelstrom`。

重点关注：`unique ID generation`、`Maelstrom workload`、`linearizability`、`HLC integration`。

建议先按提示逐步实现：Combine HLC timestamp，包含node_id用于globally unique IDs。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Integrate HLC-based IDs into the Maelstrom `generate` workload. Each generated ID must be globally unique across all 节点和should preserve causal ordering.

ID format: `"{pt}_{lc}_{node_id}"` (e.g., "1704067200001_0_n1")

Implement the standard Maelstrom `generate` handler:
```JSON
请求:  {"type": "generate", "msg_id": 1}
响应: {"type": "generate_ok", "in_reply_to": 1, "id": "1704067200001_0_n1"}
```

Also implement `parse_hlc_id` to decompose an HLC ID:
```JSON
请求:  {"type": "parse_hlc_id", "msg_id": 2, "id": "1704067200001_3_n2"}
响应: {"type": "parse_hlc_id_ok", "in_reply_to": 2, "pt": 1704067200001, "lc": 3, "节点": "n2"}
```

## 涉及概念

- `unique ID generation`
- `Maelstrom workload`
- `linearizability`
- `HLC integration`

## 实现提示

- Combine HLC timestamp，包含node_id用于globally unique IDs
-格式: pt_lc_nodeId ensures uniqueness across 节点
- HLC guarantees monotonicity even，包含时钟 skew
- The Maelstrom generate workload requires globally unique IDs
- Verify uniqueness by collecting IDs from all 节点

## 测试用例

### 1. Generate produces HLC-formatted ID

generate_ok should have id matching pattern "\d+_\d+_n1".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Parse HLC ID extracts components

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"parse_hlc_id","msg_id":2,"id":"1704067200001_3_n2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "parse_hlc_id_ok", "pt": 1704067200001, "lc": 3, "node": "n2", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Spanner: Google Globally Distributed Database](https://research.google/pubs/pub39966/)：Google Spanner paper on TrueTime和clocks

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
