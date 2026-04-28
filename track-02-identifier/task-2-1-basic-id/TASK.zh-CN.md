# 用节点标识和时间戳生成唯一 ID

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-1-basic-id>

课程：2. 标识符：分布式唯一 ID
任务序号：1
短标题：基础 ID 生成
难度：入门
子主题：为什么唯一 ID 这么难

## 中文导读

这道题要求你实现一个最基础的唯一 ID 生成器：把节点标识和时间戳拼在一起，生成不会重复的 ID。这是分布式系统中 ID 生成的第一步，理解它能帮你认识到"多台机器同时生成 ID"这件事为什么不简单。

## 题目说明

在分布式系统中，每个实体、事件和消息都需要一个唯一标识符（Unique ID）。由于没有一个统一的中心服务来分配 ID，每个节点（Node）必须独立生成 ID，同时还要避免和其他节点产生冲突。

请实现一个 `generate` 消息处理器，当收到 `generate` 请求时，返回一个唯一的 ID：

```json
{
  "type": "generate",
  "msg_id": 1
}
```

你的响应格式如下：

```json
{
  "type": "generate_ok",
  "msg_id": 1,
  "in_reply_to": 1,
  "id": "unique-id-here"
}
```

在这个最基础的实现中，将你的 `node_id` 和时间戳拼接起来生成 ID。这样做可以保证：不同节点有不同的 `node_id`，同一个节点在不同时间有不同的时间戳，从而实现唯一性。

## 概念说明

### 为什么唯一 ID 很重要

每一条数据库记录、每一行日志、每一条消息都需要一个标识符。在分布式系统中，你不能简单地用一个自增计数器来生成 ID，因为多个节点可能在同一时刻生成相同的数字。

### 冲突问题

想象一下最简单的"计数器"方案：

```text
Node A: counter = 1 → generates ID 1
Node B: counter = 1 → generates ID 1  // COLLISION!
```

两个节点生成了相同的 ID，原因就是它们之间没有任何协调。这就好比两个人各自从 1 开始编号，必然会出现重复。

### 基于时间戳的 ID

时间戳天然地提供了时间维度上的唯一性和排序能力，但两个节点可能在同一毫秒产生相同的时间戳。通过在 ID 中加入 `node_id`，就能保证跨节点的唯一性：

```text
ID = "{node_id}-{timestamp}"

Node A: "n1-1704067200000"
Node B: "n2-1704067200000"  // Different node_id = unique
```

### 遗留的挑战

不过，同一个节点在同一毫秒内多次调用，仍然可能生成重复的 ID。我们将在下一道题中解决这个问题。

## 涉及概念

- `unique IDs`
- `timestamps`
- `node identity`

## 实现提示

- 将 `node_id` 和时间戳组合起来，实现基本的唯一性
- 建议使用毫秒级精度的时间戳
- 推荐格式：`node_id-timestamp-sequence`

## 测试用例

### 1. 初始化后生成单个 ID

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

- [Unique ID Generation Challenge](https://fly.io/dist-sys/2/)：Fly.io Gossip Glomers 唯一 ID 生成挑战的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
