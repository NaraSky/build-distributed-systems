# 实现 向量 Clocks

英文标题：Implement Vector Clocks
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-3-vector-clock>

课程：2. 标识符：分布式唯一 ID
任务序号：13
短标题：向量 时钟
难度：advanced
子主题：Logical Clocks as IDs

## 中文导读

本题要求你完成 `实现 向量 Clocks`。

重点关注：`vector clock`、`causality tracking`、`element-wise max`、`concurrent detection`。

建议先按提示逐步实现：Each 节点 maintains a vector of N counters, one per 节点 in the 集群。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Vector clocks solve the limitation of Lamport clocks: they can detect **concurrent events**. Each 节点 maintains a vector of N counters (one per 节点). The rules are:

1. On **local event** or **send**: increment your own slot in the vector
2. On **receive**: take element-wise max of local和received vectors, then increment your own slot

Two events are concurrent if neither vector dominates the other: A || B when A[i] > B[i]用于some i,和A[j] < B[j]用于some j.

Implement a `vc_tick` handler:
```JSON
请求:  {"type": "vc_tick", "msg_id": 1}
响应: {"type": "vc_tick_ok", "in_reply_to": 1, "vector": {"n1": 1, "n2": 0}}
```

And a `vc_receive` handler that merges an incoming vector:
```JSON
请求:  {"type": "vc_receive", "msg_id": 2, "vector": {"n1": 0, "n2": 3}}
响应: {"type": "vc_receive_ok", "in_reply_to": 2, "vector": {"n1": 2, "n2": 3}}
```

## 涉及概念

- `vector clock`
- `causality tracking`
- `element-wise max`
- `concurrent detection`

## 实现提示

- Each 节点 maintains a vector of N counters, one per 节点 in the 集群
- On local event or send: increment your own slot
- On receive: element-wise max, then increment your own slot
- Vector clocks can distinguish concurrent events from causal ones
- Initialize the vector，包含zeros用于all known 节点 IDs

## 测试用例

### 1. Tick increments own slot

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_tick","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_tick_ok", "vector": {"n1": 1, "n2": 0}, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Merge takes element-wise max和increments own

After tick n1=1,n2=0. Merge，包含{n1:0,n2:5} -> max -> {n1:1,n2:5}, then increment own -> {n1:2,n2:5}.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"vc_receive","msg_id":3,"vector":{"n1":0,"n2":5}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_tick_ok", "vector": {"n1": 1, "n2": 0}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "vc_receive_ok", "vector": {"n1": 2, "n2": 5}, "in_reply_to": 3, "msg_id": 2}}
```

## 参考资料

- [Vector Clocks Revisited](https://riak.com/posts/technical/vector-clocks-revisited/)：Riak documentation on practical use of vector clocks

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
