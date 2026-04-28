# 通过 Maelstrom G-Counter 测试

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-5-maelstrom-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：10
短标题：Maelstrom 计数器
难度：高级
子主题：G-Counter 与 PN-Counter

## 中文导读

这道题是对你的 CRDT 计数器实现的终极正确性检验。Maelstrom 的 g-counter 工作负载会在模拟的分布式环境中运行你的节点，验证计数器在并发操作下是否行为正确。通过这个测试，意味着你的 CRDT 实现在工程上是可靠的。

## 题目说明

Maelstrom 的 g-counter 工作负载是检验你的 CRDT 计数器实现是否正确的权威测试。它会在一个模拟的分布式环境中运行你的节点，并验证计数器在并发操作下的行为是否正确。

**工作负载操作**：
- `add`：将计数器增加一个 delta 值
- `read`：返回计数器的当前值

**检查器验证的性质**：
1. 每次读取的值都不超过所有 add 操作的总和（不会多计）
2. 计数器必须是最终一致的（所有节点最终收敛到相同的值）
3. 计数器在每个节点上必须单调不减（G-Counter 的性质）

**运行测试的命令**：
```
maelstrom test -w g-counter --bin your_node --node-count 3 --rate 100 --time-limit 20
```

```json
Request:  {"type": "add", "msg_id": 1, "delta": 5}
Response: {"type": "add_ok", "in_reply_to": 1}

Request:  {"type": "read", "msg_id": 2}
Response: {"type": "read_ok", "in_reply_to": 2, "value": 42}
```

## 涉及概念

- `Maelstrom`
- `g-counter workload`
- `correctness verification`
- `linearizability check`
- `distributed testing`

## 实现提示

- Maelstrom 的 g-counter 工作负载会向你的节点发送 add 和 read 操作
- 你的实现必须处理：init、add（带 delta 参数）、read
- 节点之间必须通过 gossip 协议同步状态，以确保最终一致性
- 检查器会验证：读取值永远不会超过所有 add 操作的总和
- 可以使用前一道题的 PN-Counter 实现作为基础

## 测试用例

### 1. 加法和读取操作

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

### 2. 读取值不超过所有加法的总和

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

- [Maelstrom G-Counter](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-g-counter)：Maelstrom 关于 g-counter 工作负载的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
