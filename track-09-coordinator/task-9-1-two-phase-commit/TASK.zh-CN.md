# 实现 Two-Phase Commit

英文标题：Implement Two-Phase Commit
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-1-two-phase-commit>

课程：9. 协调器：分布式事务
任务序号：1
短标题：2PC
难度：advanced
子主题：Two-Phase Commit

## 中文导读

本题要求你完成 `实现 Two-Phase Commit`。

重点关注：`2PC`、`atomic commit`、`prepare-commit`。

建议先按提示逐步实现：Phase 1: Prepare - ask all participants。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement 2PC: Phase 1 sends PREPARE, collects votes. Phase 2 sends COMMIT if all YES, else ABORT.

## 概念说明

### Two-Phase Commit

2PC ensures all-or-nothing across 节点. The blocking problem: if coordinator crashes after PREPARE, participants are stuck.

## 涉及概念

- `2PC`
- `atomic commit`
- `prepare-commit`

## 实现提示

- Phase 1: Prepare - ask all participants
- Phase 2: Commit/Abort based on votes
- 日志 decisions用于recovery

## 测试用例

### 1. All participants vote yes

Coordinator sends PREPARE to all participants (p1, p2, p3). All vote YES. Coordinator decides COMMIT和sends to all.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [DDIA Chapter 9](https://dataintensive.net/)：Consistency和共识

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
