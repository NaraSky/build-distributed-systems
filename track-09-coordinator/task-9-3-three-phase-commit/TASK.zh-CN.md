# 实现三阶段提交

英文标题：Implement Three-Phase Commit
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-3-three-phase-commit>

课程：9. 协调器：分布式事务
任务序号：3
短标题：3PC
难度：高级
子主题：Two-Phase Commit

## 中文导读

本题要求你实现三阶段提交（3PC）协议。三阶段提交在两阶段提交的基础上增加了 PRE-COMMIT 阶段，目的是减少协调者崩溃时参与者被阻塞的情况。理解三阶段提交有助于你认识到分布式提交协议的设计取舍。

## 题目说明

三阶段提交在两阶段提交的基础上新增了 PRE-COMMIT 阶段。当协调者在 PRE-COMMIT 之后崩溃时，参与者可以安全地自行提交事务，而不需要等待协调者恢复。

## 概念说明

### 三阶段提交

三阶段提交（3PC）通过增加 PRE-COMMIT 阶段来减少阻塞问题。处于 PRE-COMMIT 状态的参与者知道所有人都已经投了赞成票，因此即使协调者崩溃，它们也可以安全地继续提交，不会出现不一致。

## 涉及概念

- `3PC`
- `non-blocking`
- `pre-commit`

## 实现提示

- 增加 PRE-COMMIT 阶段
- PRE-COMMIT 表示协调者打算提交
- 收到 PRE-COMMIT 的参与者即使失去协调者也可以自行推进

## 测试用例

### 1. 第一阶段：准备

协调者 n1 向所有参与者（n2、n3、n4）发送准备请求，全部投赞成票。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"3pc_prepare","msg_id":2,"tx_id":"tx1","participants":["n2","n3","n4"],"operations":[{"key":"x","value":10}]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"3pc_prepare_ok","in_reply_to":2,"msg_id":1,"tx_id":"tx1","votes":{"n2":"yes","n3":"yes","n4":"yes"}}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
