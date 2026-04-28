# Pass the Maelstrom G-计数器 Workload

英文标题：Pass the Maelstrom G-Counter Workload
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-5-maelstrom-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：10
短标题：Maelstrom 计数器
难度：advanced
子主题：G-计数器和PN-计数器

## 中文导读

本题要求你完成 `Pass the Maelstrom G-计数器 Workload`。

重点关注：`Maelstrom`、`g-counter workload`、`correctness verification`、`linearizability check`、`distributed testing`。

建议先按提示逐步实现：The Maelstrom g-计数器 workload sends add和read operations to your 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The Maelstrom g-计数器 workload is the definitive correctness test用于your CRDT 计数器 implementation. It runs your 节点 in a simulated distributed environment和verifies that the 计数器 behaves correctly under concurrent operations.

**Workload operations**:
- `add`: increment the 计数器 by a delta value
- `read`: return the current 计数器 value

**Checker properties**:
1. Every read value must be <= the sum of all add operations (no over-counting)
2. The 计数器 must be eventually consistent (all 节点 converge to the same value)
3. The 计数器 must be monotonically non-decreasing per 节点 (G-计数器 property)

**Running the test**:
```
Maelstrom test -w g-计数器 --bin your_node --节点-count 3 --rate 100 --time-limit 20
```

```JSON
请求:  {"type": "add", "msg_id": 1, "delta": 5}
响应: {"type": "add_ok", "in_reply_to": 1}

请求:  {"type": "read", "msg_id": 2}
响应: {"type": "read_ok", "in_reply_to": 2, "value": 42}
```

## 涉及概念

- `Maelstrom`
- `g-counter workload`
- `correctness verification`
- `linearizability check`
- `distributed testing`

## 实现提示

- The Maelstrom g-计数器 workload sends add和read operations to your 节点
- Your implementation must handle: init, add (delta), read
- 节点 must gossip state to ensure 最终一致性 across the 集群
- The checker verifies: reads never exceed the sum of all adds
- Use the PN-计数器 implementation from the previous task as the foundation

## 测试用例

### 1. 添加和read operations

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":5}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 3, "value": 5, "msg_id": 2}}
```

### 2. Read never exceeds total adds

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":10}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":3,"delta":20}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 4, "value": 30, "msg_id": 3}}
```

## 参考资料

- [Maelstrom G-Counter](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-g-counter)：Maelstrom documentation on the g-计数器 workload

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
