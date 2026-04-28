# 基于混合逻辑时钟生成全局唯一标识

英文标题：HLC-Based Unique ID Generation for Maelstrom
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-5-hlc-unique-ids>

课程：2. 标识符：分布式唯一 ID
任务序号：20
短标题：混合逻辑时钟唯一标识
难度：高级
子主题：Hybrid Logical Clocks (HLC)

## 中文导读

本题要求你将混合逻辑时钟与 Maelstrom 的标识生成工作负载集成起来。每个生成的标识必须在所有节点间全局唯一，同时保持因果顺序。这是对前面所学混合逻辑时钟知识的综合实战应用。

## 题目说明

将基于混合逻辑时钟的标识集成到 Maelstrom 的 `generate` 工作负载中。每个生成的标识必须在所有节点间全局唯一，并且应当保留因果顺序。

标识格式为：`"{pt}_{lc}_{node_id}"`（例如 "1704067200001_0_n1"）

这个格式的设计思路是：物理时间保证了大致的时间顺序，逻辑计数器保证了同一毫秒内的区分度，节点标识保证了不同节点之间不会冲突。三者组合在一起，就得到了全局唯一且有序的标识。

实现标准的 Maelstrom `generate` 处理器：
```json
请求:  {"type": "generate", "msg_id": 1}
响应: {"type": "generate_ok", "in_reply_to": 1, "id": "1704067200001_0_n1"}
```

同时实现 `parse_hlc_id` 处理器，用于将一个混合逻辑时钟标识拆解为各个组成部分：
```json
请求:  {"type": "parse_hlc_id", "msg_id": 2, "id": "1704067200001_3_n2"}
响应: {"type": "parse_hlc_id_ok", "in_reply_to": 2, "pt": 1704067200001, "lc": 3, "node": "n2"}
```

## 涉及概念

- `unique ID generation`
- `Maelstrom workload`
- `linearizability`
- `HLC integration`

## 实现提示

- 将混合逻辑时钟的时间戳与节点标识组合，即可生成全局唯一的标识
- 格式 pt_lc_nodeId 保证了跨节点的唯一性
- 混合逻辑时钟即使在时钟偏差的情况下也能保证单调递增
- Maelstrom 的 generate 工作负载要求标识在全局范围内唯一
- 可以收集所有节点生成的标识来验证唯一性

## 测试用例

### 1. 生成符合混合逻辑时钟格式的标识

`generate_ok` 响应中的 id 应匹配模式 "\d+_\d+_n1"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 解析混合逻辑时钟标识并提取各组成部分

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

- [Spanner: Google Globally Distributed Database](https://research.google/pubs/pub39966/)：Google Spanner 论文，介绍了 TrueTime 和时钟机制

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
