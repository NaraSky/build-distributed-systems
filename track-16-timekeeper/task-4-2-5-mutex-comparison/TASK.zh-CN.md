# Compare Mutex Algorithms: Lamport vs Token Ring vs Centralized

英文标题：Compare Mutex Algorithms: Lamport vs Token Ring vs Centralized
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-5-mutex-comparison>

课程：16. 时间守卫：逻辑时钟
任务序号：10
短标题：Mutex Comparison
难度：advanced
子主题：Lamport Clocks

## 中文导读

本题要求你完成 `Compare Mutex Algorithms: Lamport vs Token Ring vs Centralized`。

重点关注：`message complexity`、`token ring`、`centralized mutex`、`algorithm comparison`。

建议先按提示逐步实现：Lamport mutex: 3(N-1) 消息 per critical section entry (请求 + reply + release)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Different distributed mutex algorithms have different tradeoffs. Compare three approaches:

1. **Lamport's algorithm**: 3(N-1) 消息 per CS entry, fully distributed, fair
2. **Token ring**: 0 to N-1 消息, no starvation, but token can be lost
3. **Centralized**: 3 消息, simple, but coordinator is a single point of 故障

Implement a `compare_mutex` handler:
```JSON
请求:  {"type": "compare_mutex", "msg_id": 1, "节点": 5}
响应: {"type": "compare_mutex_ok", "in_reply_to": 1, "comparison": [
    {"algorithm": "lamport", "messages_per_cs": 12, "fault_tolerant": true, "fair": true},
    {"algorithm": "token_ring", "messages_per_cs_avg": 2.5, "fault_tolerant": false, "fair": true},
    {"algorithm": "centralized", "messages_per_cs": 3, "fault_tolerant": false, "fair": true}
]}
```

Also implement a `simulate_token_ring` handler:
```JSON
请求:  {"type": "simulate_token_ring", "msg_id": 2, "节点": 5, "requests": ["n3", "n1"]}
响应: {"type": "simulate_token_ring_ok", "in_reply_to": 2, "total_messages": 5, "grant_order": ["n3", "n1"]}
```

## 涉及概念

- `message complexity`
- `token ring`
- `centralized mutex`
- `algorithm comparison`

## 实现提示

- Lamport mutex: 3(N-1) 消息 per critical section entry (请求 + reply + release)
- Token ring: 0 to N-1 消息 per entry (depends on token position)
- Centralized: 3 消息 per entry (请求 + grant + release) but single point of 故障
- Compare on: 消息 count, 故障 tolerance, fairness,和latency
- Build a comparison table，包含all metrics

## 测试用例

### 1. Compare mutex用于5 nodes

compare_mutex_ok，包含3 algorithm entries. Lamport messages_per_cs = 3*(5-1) = 12.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_mutex","msg_id":2,"nodes":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compare mutex用于10 nodes

Lamport messages_per_cs = 3*(10-1) = 27. Centralized stays at 3.

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

- [Comparison of Mutual Exclusion Algorithms](https://www.geeksforgeeks.org/mutual-exclusion-in-distributed-system/)：Comparison table of distributed mutex algorithms

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
