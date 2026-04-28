# Compare HLC, UUID v4,和Snowflake IDs

英文标题：Compare HLC, UUID v4,和Snowflake IDs
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-4-id-comparison>

课程：2. 标识符：分布式唯一 ID
任务序号：19
短标题：ID Comparison
难度：intermediate
子主题：混合逻辑 Clocks (HLC)

## 中文导读

本题要求你完成 `Compare HLC, UUID v4,和Snowflake IDs`。

重点关注：`UUID`、`Snowflake`、`HLC`、`ID tradeoffs`、`benchmarking`。

建议先按提示逐步实现：UUID v4 is random: 128 bits, no ordering, no coordination needed。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Different ID schemes have different tradeoffs. Your task is to implement all three和return a comparison table.

Implement a `compare_ids` handler that generates one ID of each type和reports their properties:

```JSON
请求:  {"type": "compare_ids", "msg_id": 1}
响应: {"type": "compare_ids_ok", "in_reply_to": 1, "comparison": [
    {"scheme": "uuid_v4", "id": "550e8400-e29b...", "bits": 128, "sortable": false, "causal": false},
    {"scheme": "snowflake", "id": "7041429939834880", "bits": 64, "sortable": true, "causal": false},
    {"scheme": "hlc", "id": "1234567-0-n1", "bits": 96, "sortable": true, "causal": true}
]}
```

## 涉及概念

- `UUID`
- `Snowflake`
- `HLC`
- `ID tradeoffs`
- `benchmarking`

## 实现提示

- UUID v4 is random: 128 bits, no ordering, no coordination needed
- Snowflake is timestamped: 64 bits, sorted, needs machine_id assignment
- HLC is timestamped + causal: variable size, captures causality, needs 时钟 sync
- Compare: 存储 size, generation speed, uniqueness guarantee, sortability
- Each approach has different tradeoffs用于different use cases

## 测试用例

### 1. Compare IDs returns three schemes

compare_ids_ok should contain a comparison array，包含3 entries: uuid_v4, snowflake,和hlc. Each has id, bits, sortable,和causal fields.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_ids","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [UUID Versions Explained](https://www.ietf.org/rfc/rfc4122.txt)：RFC 4122 defining UUID format和versions

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
