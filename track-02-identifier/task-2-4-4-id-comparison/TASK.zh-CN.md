# 比较三种分布式标识方案

英文标题：Compare HLC, UUID v4, and Snowflake IDs
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-4-id-comparison>

课程：2. 标识符：分布式唯一 ID
任务序号：19
短标题：标识方案对比
难度：进阶
子主题：Hybrid Logical Clocks (HLC)

## 中文导读

分布式系统中有多种标识生成方案，各有优劣。本题要求你分别实现 UUID v4、Snowflake 和混合逻辑时钟三种方案，并生成一张对比表，帮助你理解不同场景下应该选择哪种方案。这是对整个标识课程的综合总结。

## 题目说明

不同的标识生成方案有着不同的权衡取舍。你的任务是实现三种方案，并返回一张对比表。

实现 `compare_ids` 处理器，分别生成三种类型的标识，并报告它们的属性：

```json
请求:  {"type": "compare_ids", "msg_id": 1}
响应: {"type": "compare_ids_ok", "in_reply_to": 1, "comparison": [
    {"scheme": "uuid_v4", "id": "550e8400-e29b...", "bits": 128, "sortable": false, "causal": false},
    {"scheme": "snowflake", "id": "7041429939834880", "bits": 64, "sortable": true, "causal": false},
    {"scheme": "hlc", "id": "1234567-0-n1", "bits": 96, "sortable": true, "causal": true}
]}
```

三种方案简要对比如下：
- **UUID v4**：纯随机生成，128 位，不可排序，不需要节点间协调
- **Snowflake**：基于时间戳，64 位，可排序，需要分配机器编号
- **混合逻辑时钟**：时间戳加因果关系，可变大小，可排序，还能追踪因果关系

## 涉及概念

- `UUID`
- `Snowflake`
- `HLC`
- `ID tradeoffs`
- `benchmarking`

## 实现提示

- UUID v4 是纯随机的：128 位，没有排序能力，不需要协调
- Snowflake 是基于时间戳的：64 位，可排序，需要分配机器编号
- 混合逻辑时钟包含时间戳和因果信息：可变大小，能捕获因果关系，需要时钟同步
- 可以从以下维度进行比较：存储大小、生成速度、唯一性保证、可排序性
- 每种方案适用于不同的使用场景

## 测试用例

### 1. 对比接口返回三种方案

`compare_ids_ok` 响应应包含一个具有 3 个条目的对比数组，分别是 uuid_v4、snowflake 和 hlc。每个条目都有 id、bits、sortable 和 causal 字段。

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

- [UUID Versions Explained](https://www.ietf.org/rfc/rfc4122.txt)：定义 UUID 格式和版本的 RFC 4122 标准文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
