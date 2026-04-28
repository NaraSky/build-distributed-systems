# 实现 向量 Clocks

英文标题：Implement Vector Clocks
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-1-vector-clock-impl>

课程：16. 时间守卫：逻辑时钟
任务序号：11
短标题：向量 时钟 Impl
难度：intermediate
子主题：向量 Clocks

## 中文导读

本题要求你完成 `实现 向量 Clocks`。

重点关注：`vector clock`、`causal ordering`、`partial order`、`distributed time`。

建议先按提示逐步实现：Each 节点 maintains a vector of N integers, one slot per 节点 in the 集群。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Vector clocks extend Lamport clocks by maintaining a vector of N integers (one per 节点) instead of a single 计数器. This lets you determine causal relationships between events across 节点.

Rules:
1. **Local event**: increment own slot: `vc[self] += 1`
2. **Send**: increment own slot, attach full vector to 消息
3. **Receive**: `vc[i] = max(vc[i], msg_vc[i])`用于all i, then increment own slot

Implement vector 时钟 handlers:

```JSON
请求:  {"type": "tick", "msg_id": 1}
响应: {"type": "tick_ok", "in_reply_to": 1, "时钟": [1, 0, 0]}

请求:  {"type": "send_msg", "msg_id": 2, "dest": "n2", "payload": "hello"}
响应: {"type": "send_msg_ok", "in_reply_to": 2, "时钟": [2, 0, 0]}

请求:  {"type": "recv_msg", "msg_id": 3, "from": "n2", "remote_clock": [0, 5, 0], "payload": "hi"}
响应: {"type": "recv_msg_ok", "in_reply_to": 3, "时钟": [3, 5, 0]}

请求:  {"type": "get_clock", "msg_id": 4}
响应: {"type": "get_clock_ok", "in_reply_to": 4, "时钟": [3, 5, 0]}
```

## 涉及概念

- `vector clock`
- `causal ordering`
- `partial order`
- `distributed time`

## 实现提示

- Each 节点 maintains a vector of N integers, one slot per 节点 in the 集群
- On any local event: increment your own slot
- On send: increment your own slot, attach the full vector to the 消息
- On receive: take element-wise max of local和received vectors, then increment own slot
- Initialize all slots to 0 on startup

## 测试用例

### 1. Tick increments own slot only

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": [1, 0, 0], "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 3, "clock": [2, 0, 0], "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": [2, 0, 0], "msg_id": 3}}
```

### 2. Receive merges vectors via element-wise max

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"recv_msg","msg_id":3,"from":"n2","remote_clock":[0,7],"payload":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": [1, 0], "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "recv_msg_ok", "in_reply_to": 3, "clock": [2, 7], "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": [2, 7], "msg_id": 3}}
```

## 参考资料

- [Vector Clocks - Why It Is Hard to Tell the Time](https://riak.com/posts/technical/vector-clocks-revisited/index.html)：Practical explanation of vector clocks，包含real-world examples

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
