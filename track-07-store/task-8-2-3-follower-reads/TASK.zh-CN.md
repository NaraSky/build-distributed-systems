# 添加 Follower Reads，包含Bounded Staleness

英文标题：Add Follower Reads，包含Bounded Staleness
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-3-follower-reads>

课程：7. 存储：线性一致 KV Store
任务序号：8
短标题：Follower Reads
难度：advanced
子主题：Read Optimization

## 中文导读

本题要求你完成 `添加 Follower Reads，包含Bounded Staleness`。

重点关注：`follower reads`、`bounded staleness`、`read scalability`、`consistency tradeoff`。

建议先按提示逐步实现：Clients opt in to reading from followers if they accept data up to T seconds stale。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement Follower reads，包含bounded staleness. Clients can opt to read from any Follower if they accept data up to T seconds stale. This scales read throughput linearly，包含集群 size.

```JSON
请求:  {"type": "follower_read", "msg_id": 1, "key": "x", "max_staleness_ms": 5000}
响应: {"type": "follower_read_ok", "in_reply_to": 1, "value": "42", "actual_staleness_ms": 200, "served_by": "n2", "线性一致": false}

请求:  {"type": "follower_read", "msg_id": 2, "key": "x", "max_staleness_ms": 0}
响应: {"type": "follower_read_ok", "in_reply_to": 2, "value": "42", "served_by": "n1", "线性一致": true, "reason": "redirected_to_leader"}
```

## 涉及概念

- `follower reads`
- `bounded staleness`
- `read scalability`
- `consistency tradeoff`

## 实现提示

- Clients opt in to reading from followers if they accept data up to T seconds stale
- Followers track their applied 索引; reads are served if the data is fresh enough
- This distributes read load across all replicas, not just the Leader
- The staleness bound is configurable per-请求
- Compare latency: Follower reads avoid the Leader bottleneck

## 测试用例

### 1. Follower read within staleness bound

follower_read_ok，包含actual_staleness_ms <= 5000. 线性一致: false.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"follower_read","msg_id":2,"key":"x","max_staleness_ms":5000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Zero staleness redirects to Leader

With max_staleness_ms: 0, read should be served by Leader. 线性一致: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"follower_read","msg_id":2,"key":"x","max_staleness_ms":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [CockroachDB Follower Reads](https://www.cockroachlabs.com/docs/stable/follower-reads.html)：How CockroachDB implements Follower reads用于geo-分布式系统

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
