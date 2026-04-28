# 实现 Byzantine Fault Tolerance

英文标题：Implement Byzantine Fault Tolerance
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-3-pbft>

课程：10. 高级主题
任务序号：3
短标题：PBFT
难度：advanced
子主题：高级 Paradigms

## 中文导读

本题要求你完成 `实现 Byzantine Fault Tolerance`。

重点关注：`Byzantine`、`PBFT`、`f faults`。

建议先按提示逐步实现：Need 3f+1 节点 to tolerate f faults。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement PBFT: tolerates f Byzantine faults，包含3f+1 节点. Three phases: pre-prepare, prepare, commit.

## 概念说明

### Byzantine Fault Tolerance

Byzantine faults include malicious behavior. PBFT requires 3f+1 节点 to tolerate f faulty 节点. Uses 3 phases，包含quorum certificates.

## 涉及概念

- `Byzantine`
- `PBFT`
- `f faults`

## 实现提示

- Need 3f+1 节点 to tolerate f faults
- Pre-prepare, Prepare, Commit phases
- Wait用于2f+1 matching 消息

## 测试用例

### 1. Pre-prepare phase

Multi-节点 test: 4 节点 (n=4, f=1, need 2f+1=3用于quorum). Primary (n0) receives 客户端 请求 seq=1. Primary broadcasts PRE-PREPARE to all replicas (n1, n2, n3)，包含sequence number, digest,和view. Verify all replicas receive pre-prepare 消息.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [PBFT Paper](http://pmg.csail.mit.edu/papers/osdi99.pdf)：Practical Byzantine 故障 Tolerance

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
