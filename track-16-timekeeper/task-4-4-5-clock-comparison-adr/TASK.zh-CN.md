# Architecture Decision Record: Choosing a 时钟 System

英文标题：Architecture Decision Record: Choosing a Clock System
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-5-clock-comparison-adr>

课程：16. 时间守卫：逻辑时钟
任务序号：20
短标题：时钟 ADR
难度：advanced
子主题：混合逻辑 Clocks

## 中文导读

本题要求你完成 `Architecture Decision Record: Choosing a 时钟 System`。

重点关注：`architecture decision record`、`clock comparison`、`multi-region`、`tradeoffs`。

建议先按提示逐步实现：Compare HLC, UUID v4, Snowflake, Lamport,和Vector Clocks across multiple dimensions。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Write an Architecture Decision Record (ADR)用于choosing a 时钟 system用于a multi-region distributed database. Compare five 时钟 systems across multiple dimensions.

Implement a `compare_clocks` handler that generates the comparison table,和a `generate_adr` handler that produces the decision record:

```JSON
请求:  {"type": "compare_clocks", "msg_id": 1}
响应: {"type": "compare_clocks_ok", "in_reply_to": 1, "comparison": [
    {"system": "uuid_v4", "uniqueness": "global", "causality": "none", "size_bytes": 16, "speed_ns": 50},
    {"system": "snowflake", "uniqueness": "global", "causality": "partial_within_node", "size_bytes": 8, "speed_ns": 10},
    {"system": "lamport", "uniqueness": "none", "causality": "partial", "size_bytes": 8, "speed_ns": 5},
    {"system": "vector_clock", "uniqueness": "none", "causality": "full", "size_bytes": "8*N", "speed_ns": 10},
    {"system": "hlc", "uniqueness": "global_with_node", "causality": "full", "size_bytes": 12, "speed_ns": 15}
]}

请求:  {"type": "generate_adr", "msg_id": 2, "use_case": "multi_region_database", "regions": 3}
响应: {"type": "generate_adr_ok", "in_reply_to": 2, "decision": "hlc", "rationale": "...", "tradeoffs": ["..."], "status": "accepted"}
```

## 涉及概念

- `architecture decision record`
- `clock comparison`
- `multi-region`
- `tradeoffs`

## 实现提示

- Compare HLC, UUID v4, Snowflake, Lamport,和Vector Clocks across multiple dimensions
- Dimensions: uniqueness, causality encoding, 存储 size, generation speed, cross-region behavior
- For a multi-region database, HLC is the best fit because it gives both causality和time proximity
- UUID v4 gives uniqueness but no ordering; Snowflake gives ordering but no causality
- Write a structured ADR: Context, Decision, Status, Consequences

## 测试用例

### 1. Compare all 时钟 systems

compare_clocks_ok should contain 5 entries covering uuid_v4, snowflake, lamport, vector_clock,和hlc，包含correct properties.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_clocks","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. ADR用于multi-region database recommends HLC

generate_adr_ok should recommend HLC用于multi-region database，包含rationale covering causality和time proximity.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate_adr","msg_id":2,"use_case":"multi_region_database","regions":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Architecture Decision Records](https://adr.github.io/)：How to write和maintain Architecture Decision Records
- [Spanner: Google Globally-Distributed Database](https://research.google/pubs/pub39966/)：The Spanner paper showing TrueTime和its 时钟 system tradeoffs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
