# 实现 Three-Phase Commit

英文标题：Implement Three-Phase Commit
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-3-three-phase-commit>

课程：9. 协调器：分布式事务
任务序号：3
短标题：3PC
难度：advanced
子主题：Two-Phase Commit

## 中文导读

本题要求你完成 `实现 Three-Phase Commit`。

重点关注：`3PC`、`non-blocking`、`pre-commit`。

建议先按提示逐步实现：Add PRE-COMMIT phase。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

3PC adds PRE-COMMIT phase. If coordinator fails after PRE-COMMIT, participants can commit safely.

## 概念说明

### Three-Phase Commit

3PC reduces blocking by adding PRE-COMMIT. Participants in PRE-COMMIT know decision was commit if coordinator fails.

## 涉及概念

- `3PC`
- `non-blocking`
- `pre-commit`

## 实现提示

- Add PRE-COMMIT phase
- PRE-COMMIT indicates intent to commit
- Participants can proceed without coordinator

## 测试用例

### 1. Phase 1: Prepare

Coordinator n1 sends prepare to all participants (n2, n3, n4). All vote YES.

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
