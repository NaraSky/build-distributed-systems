# 实现两阶段提交

英文标题：Implement Two-Phase Commit
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-1-two-phase-commit>

课程：9. 协调器：分布式事务
任务序号：1
短标题：2PC
难度：高级
子主题：Two-Phase Commit

## 中文导读

本题要求你实现两阶段提交（2PC）协议，这是分布式系统中保证多个节点"要么全部提交、要么全部回滚"的经典方案。理解两阶段提交是学习分布式事务的第一步，也是后续理解三阶段提交和共识算法的基础。

## 题目说明

实现两阶段提交协议。第一阶段，协调者（Coordinator）向所有参与者（Participant）发送 PREPARE 消息，收集它们的投票结果。第二阶段，如果所有参与者都投了赞成票（YES），协调者就发送 COMMIT 指令；只要有一个参与者投了反对票（NO），协调者就发送 ABORT 指令，中止整个事务。

## 概念说明

### 两阶段提交

两阶段提交（2PC）保证了分布式事务的原子性：多个节点（Node）上的操作，要么全部执行成功，要么全部回滚。但它有一个著名的阻塞问题：如果协调者在发出 PREPARE 之后崩溃了，参与者就会陷入"进退两难"的状态，既不知道该提交也不知道该中止，只能干等协调者恢复。

## 涉及概念

- `2PC`
- `atomic commit`
- `prepare-commit`

## 实现提示

- 第一阶段（准备阶段）：向所有参与者发送 PREPARE，询问它们是否可以提交
- 第二阶段（提交/中止阶段）：根据投票结果决定发送 COMMIT 还是 ABORT
- 将决策记录到日志中，以便故障恢复时使用

## 测试用例

### 1. 所有参与者投赞成票

协调者向所有参与者（p1、p2、p3）发送 PREPARE，全部返回 YES。协调者做出 COMMIT 决策并发送给所有参与者。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [DDIA Chapter 9](https://dataintensive.net/)：讲解一致性与共识的经典章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
