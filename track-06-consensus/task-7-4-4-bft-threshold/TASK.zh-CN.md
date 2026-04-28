# Prove the N >= 3f+1 Byzantine Fault Threshold

英文标题：Prove the N >= 3f+1 Byzantine Fault Threshold
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-4-bft-threshold>

课程：6. 共识：Raft 与日志复制
任务序号：19
短标题：BFT Threshold
难度：advanced
子主题：Byzantine Fault Tolerance

## 中文导读

本题要求你完成 `Prove the N >= 3f+1 Byzantine Fault Threshold`。

重点关注：`fault threshold`、`3f+1`、`impossibility result`、`Byzantine quorum`。

建议先按提示逐步实现：With N 节点和f Byzantine faults, correct 节点 = N - f。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Prove that tolerating f Byzantine faults requires at least N >= 3f+1 节点. Then verify empirically.

The proof:
- We need two quorums to overlap in at least f+1 节点 (to guarantee at least 1 honest overlap)
- Quorum size Q must satisfy: 2Q - N > f (overlap > f)
- Q must also be > N - f (must include more than all correct 节点 that might not respond)
- Solving: N >= 3f + 1

```JSON
请求:  {"type": "bft_threshold", "msg_id": 1, "f": 1}
响应: {"type": "bft_threshold_ok", "in_reply_to": 1, "f": 1, "min_n": 4, "quorum_size": 3, "honest_in_quorum": 2, "safe": true}

请求:  {"type": "bft_threshold", "msg_id": 2, "f": 2}
响应: {"type": "bft_threshold_ok", "in_reply_to": 2, "f": 2, "min_n": 7, "quorum_size": 5, "honest_in_quorum": 3, "safe": true}

请求:  {"type": "bft_test_insufficient", "msg_id": 3, "n": 3, "f": 1}
响应: {"type": "bft_test_insufficient_ok", "in_reply_to": 3, "sufficient": false, "reason": "3 < 3*1+1 = 4", "attack_possible": true}
```

## 涉及概念

- `fault threshold`
- `3f+1`
- `impossibility result`
- `Byzantine quorum`

## 实现提示

- With N 节点和f Byzantine faults, correct 节点 = N - f
- A quorum must be > (N + f) / 2 to guarantee overlap，包含honest 节点
- For N = 3f, you get exactly 2f correct 节点, but 2f-1 may affirm和f Byzantines may lie
- At 3f+1, a quorum of 2f+1 guarantees f+1 honest 节点 in every quorum
- Test empirically: f=1 needs N=4, f=2 needs N=7

## 测试用例

### 1. f=1 requires N=4

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bft_threshold","msg_id":2,"f":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bft_threshold_ok", "in_reply_to": 2, "f": 1, "min_n": 4, "quorum_size": 3, "honest_in_quorum": 2, "safe": true, "msg_id": 1}}
```

### 2. f=2 requires N=7

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bft_threshold","msg_id":2,"f":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bft_threshold_ok", "in_reply_to": 2, "f": 2, "min_n": 7, "quorum_size": 5, "honest_in_quorum": 3, "safe": true, "msg_id": 1}}
```

## 参考资料

- [Byzantine Fault Tolerance Bounds](https://decentralizedthoughts.github.io/2019-06-17-the-threshold-adversary/)：Why 3f+1 is the minimum用于BFT 共识

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
