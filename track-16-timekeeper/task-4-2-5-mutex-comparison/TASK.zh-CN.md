# 对比互斥算法：Lamport、令牌环与集中式

英文标题：Compare Mutex Algorithms: Lamport vs Token Ring vs Centralized
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-5-mutex-comparison>

课程：16. 时间守卫：逻辑时钟
任务序号：10
短标题：互斥算法对比
难度：高级
子主题：Lamport 时钟

## 中文导读

这道题让你对比三种经典的分布式互斥算法。Lamport 算法完全去中心化但消息开销大，令牌环（Token Ring）算法消息少但令牌可能丢失，集中式算法最简单但协调者是单点故障。没有"最好"的算法，只有最适合特定场景的算法。通过实现对比逻辑，你能直观理解它们在消息复杂度、容错性和公平性上的权衡。

## 题目说明

不同的分布式互斥算法有着不同的权衡取舍。你需要对比以下三种方案：

1. **Lamport 算法**：每次进入临界区需要 `3(N-1)` 条消息，完全去中心化，公平
2. **令牌环算法**：每次进入临界区需要 0 到 `N-1` 条消息，不会饥饿，但令牌可能丢失
3. **集中式算法**：每次进入临界区只需 3 条消息，实现简单，但协调者是单点故障

实现 `compare_mutex` 消息处理器：
```json
Request:  {"type": "compare_mutex", "msg_id": 1, "nodes": 5}
Response: {"type": "compare_mutex_ok", "in_reply_to": 1, "comparison": [
    {"algorithm": "lamport", "messages_per_cs": 12, "fault_tolerant": true, "fair": true},
    {"algorithm": "token_ring", "messages_per_cs_avg": 2.5, "fault_tolerant": false, "fair": true},
    {"algorithm": "centralized", "messages_per_cs": 3, "fault_tolerant": false, "fair": true}
]}
```

同时实现 `simulate_token_ring` 消息处理器：
```json
Request:  {"type": "simulate_token_ring", "msg_id": 2, "nodes": 5, "requests": ["n3", "n1"]}
Response: {"type": "simulate_token_ring_ok", "in_reply_to": 2, "total_messages": 5, "grant_order": ["n3", "n1"]}
```

## 涉及概念

- `message complexity`
- `token ring`
- `centralized mutex`
- `algorithm comparison`

## 实现提示

- Lamport 互斥：每次进入临界区需要 `3(N-1)` 条消息（请求 + 回复 + 释放）
- 令牌环：每次进入临界区需要 0 到 `N-1` 条消息（取决于令牌当前位置）
- 集中式：每次进入临界区需要 3 条消息（请求 + 授权 + 释放），但存在单点故障
- 从消息数量、容错性、公平性和延迟等维度进行对比
- 构建一张包含所有指标的对比表

## 测试用例

### 1. 对比 5 个节点下的互斥算法

返回的 `compare_mutex_ok` 应包含 3 种算法的条目。Lamport 算法的 `messages_per_cs = 3*(5-1) = 12`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_mutex","msg_id":2,"nodes":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 对比 10 个节点下的互斥算法

Lamport 算法的 `messages_per_cs = 3*(10-1) = 27`，而集中式算法始终为 3。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_mutex","msg_id":2,"nodes":10}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Comparison of Mutual Exclusion Algorithms](https://www.geeksforgeeks.org/mutual-exclusion-in-distributed-system/)：分布式互斥算法的对比表

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
