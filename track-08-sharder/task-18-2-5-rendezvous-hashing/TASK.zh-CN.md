# 实现 Rendezvous Hashing (Highest随机Weight)

英文标题：Implement Rendezvous Hashing (Highest随机Weight)
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-5-rendezvous-hashing>

课程：8. 分片器：水平扩展与数据迁移
任务序号：10
短标题：Rendezvous Hashing
难度：advanced
子主题：Consistent Hashing

## 中文导读

本题要求你完成 `实现 Rendezvous Hashing (Highest随机Weight)`。

重点关注：`rendezvous hashing`、`highest random weight`、`HRW`、`consistent hashing alternative`、`weighted nodes`。

建议先按提示逐步实现：For each key, compute weight(key, 节点) = hash(key + node_id)用于ALL 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Rendezvous hashing (Highest随机Weight) is an alternative to consistent hashing. For each key, compute a score用于every 节点,和the highest score wins.

**Algorithm**:
1. For each key K和each 节点 N: `score = hash(K + N)`
2. Assign K to the 节点，包含the highest score
3. When a 节点 is added/removed, re-evaluate only affected keys

**Advantages over consistent hashing**:
- Simpler implementation (no ring data structure)
- Perfect distribution without virtual 节点
- Easy to support weighted 节点: `score = hash(K + N) * weight(N)`

**Disadvantages**:
- O(N) per lookup (must compute score用于all 节点) vs. O(日志 N)用于ring
- For small clusters (<100 节点), the O(N) cost is negligible

```JSON
请求:  {"type": "hrw_lookup", "msg_id": 1, "key": "user:42", "节点": ["n1", "n2", "n3"]}
响应: {"type": "hrw_lookup_ok", "in_reply_to": 1, "key": "user:42", "winner": "n2", "scores": {"n1": 12345, "n2": 99999, "n3": 45678}}
```

## 涉及概念

- `rendezvous hashing`
- `highest random weight`
- `HRW`
- `consistent hashing alternative`
- `weighted nodes`

## 实现提示

- For each key, compute weight(key, 节点) = hash(key + node_id)用于ALL 节点
- The 节点，包含the highest weight owns the key
- When a 节点 is added/removed, only keys where that 节点 had the highest weight are affected
- Simpler than consistent hashing: no ring, no virtual 节点
- Naturally supports weighted 节点: multiply the hash by the 节点 weight

## 测试用例

### 1. HRW returns node，包含highest score

winner should be the 节点，包含the highest score in the scores map.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":2,"key":"test","nodes":["n1","n2","n3"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Same key always maps to same node

Both lookups should return the same winner.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":2,"key":"k","nodes":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":3,"key":"k","nodes":["n1","n2"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Rendezvous Hashing](https://en.wikipedia.org/wiki/Rendezvous_hashing)：Wikipedia article on rendezvous hashing (highest random weight)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
