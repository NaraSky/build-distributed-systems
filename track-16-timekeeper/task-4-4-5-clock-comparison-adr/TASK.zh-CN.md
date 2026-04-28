# 架构决策记录：选择时钟系统

英文标题：Architecture Decision Record: Choosing a Clock System
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-5-clock-comparison-adr>

课程：16. 时间守卫：逻辑时钟
任务序号：20
短标题：时钟架构决策记录
难度：高级
子主题：混合逻辑时钟

## 中文导读

本题要求你为一个多地域分布式数据库编写架构决策记录（Architecture Decision Record，简称 ADR），比较五种时钟系统的优劣并做出选择。这是一个综合性的设计思考练习，帮助你理解不同时钟方案在唯一性、因果性、存储开销、生成速度等维度上的权衡取舍。

## 题目说明

为一个多地域分布式数据库编写架构决策记录，从多个维度对比五种时钟系统。

请实现一个 `compare_clocks` 处理器用于生成对比表格，以及一个 `generate_adr` 处理器用于生成决策记录：

```json
Request:  {"type": "compare_clocks", "msg_id": 1}
Response: {"type": "compare_clocks_ok", "in_reply_to": 1, "comparison": [
    {"system": "uuid_v4", "uniqueness": "global", "causality": "none", "size_bytes": 16, "speed_ns": 50},
    {"system": "snowflake", "uniqueness": "global", "causality": "partial_within_node", "size_bytes": 8, "speed_ns": 10},
    {"system": "lamport", "uniqueness": "none", "causality": "partial", "size_bytes": 8, "speed_ns": 5},
    {"system": "vector_clock", "uniqueness": "none", "causality": "full", "size_bytes": "8*N", "speed_ns": 10},
    {"system": "hlc", "uniqueness": "global_with_node", "causality": "full", "size_bytes": 12, "speed_ns": 15}
]}

Request:  {"type": "generate_adr", "msg_id": 2, "use_case": "multi_region_database", "regions": 3}
Response: {"type": "generate_adr_ok", "in_reply_to": 2, "decision": "hlc", "rationale": "...", "tradeoffs": ["..."], "status": "accepted"}
```

## 涉及概念

- `architecture decision record`
- `clock comparison`
- `multi-region`
- `tradeoffs`

## 实现提示

- 从多个维度对比 HLC、UUID v4、Snowflake、Lamport 和向量时钟
- 比较维度包括：唯一性、因果性编码、存储大小、生成速度、跨地域行为
- 对于多地域数据库场景，HLC 是最佳选择，因为它同时提供因果性和时间接近性
- UUID v4 提供唯一性但没有排序能力；Snowflake 提供排序但没有因果性
- 按照标准结构编写架构决策记录：背景、决策、状态、后果

## 测试用例

### 1. 对比所有时钟系统

`compare_clocks_ok` 应包含 5 个条目，覆盖 uuid_v4、snowflake、lamport、vector_clock 和 hlc，每个条目都有正确的属性值。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_clocks","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 多地域数据库的架构决策记录推荐 HLC

`generate_adr_ok` 应推荐 HLC 用于多地域数据库，并给出涵盖因果性和时间接近性的理由。

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

- [Architecture Decision Records](https://adr.github.io/)：介绍如何编写和维护架构决策记录
- [Spanner: Google Globally-Distributed Database](https://research.google/pubs/pub39966/)：Google Spanner 论文，展示了 TrueTime 及其时钟系统的设计权衡

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
