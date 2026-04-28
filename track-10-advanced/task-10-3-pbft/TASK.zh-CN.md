# 实现拜占庭容错

英文标题：Implement Byzantine Fault Tolerance
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-3-pbft>

课程：10. 高级主题
任务序号：3
短标题：PBFT
难度：高级
子主题：高级范式

## 中文导读

本题要求你实现实用拜占庭容错（PBFT）算法。与之前学习的崩溃容错不同，拜占庭容错能应对节点"作恶"的情况（比如发送虚假消息）。PBFT 需要 3f+1 个节点才能容忍 f 个拜占庭故障节点，是区块链等系统的理论基础。

## 题目说明

实现 PBFT 算法：在 3f+1 个节点的系统中容忍 f 个拜占庭（Byzantine）故障节点。协议分为三个阶段：预准备（Pre-Prepare）、准备（Prepare）和提交（Commit）。

## 概念说明

### 拜占庭容错

拜占庭故障包括恶意行为，比如节点故意发送错误信息或拒绝响应。PBFT 需要 3f+1 个节点才能容忍 f 个故障节点，协议通过三个阶段和法定人数证书（Quorum Certificate）来达成共识。你可以把它理解为：即使有人在捣乱，只要捣乱的人不超过三分之一，系统仍然能正常工作。

## 涉及概念

- `Byzantine`
- `PBFT`
- `f faults`

## 实现提示

- 需要 3f+1 个节点来容忍 f 个故障节点
- 三个阶段：预准备（Pre-Prepare）、准备（Prepare）、提交（Commit）
- 等待收集到 2f+1 个一致的消息才能推进

## 测试用例

### 1. 预准备阶段

多节点测试：4 个节点（n=4，f=1，法定人数为 2f+1=3）。主节点（n0）收到客户端请求 seq=1。主节点向所有副本（n1、n2、n3）广播 PRE-PREPARE 消息，包含序列号、摘要和视图编号。验证所有副本都收到了预准备消息。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [PBFT Paper](http://pmg.csail.mit.edu/papers/osdi99.pdf)：实用拜占庭容错的原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
