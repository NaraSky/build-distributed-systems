#处理Coordinator Failure

英文标题：Handle Coordinator Failure
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-2-coordinator-failure>

课程：9. 协调器：分布式事务
任务序号：2
短标题：Coordinator Failure
难度：advanced
子主题：Two-Phase Commit

## 中文导读

本题要求你完成 `Handle Coordinator Failure`。

重点关注：`failure recovery`、`blocking`、`write-ahead log`。

建议先按提示逐步实现：日志 before sending 消息。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Handle coordinator failures: 日志 PREPARE before sending, 日志 COMMIT/ABORT decision, recover from 日志.

## 概念说明

### Write-Ahead Logging

日志 decision before sending. On recovery, read 日志 to resume. Participants in PREPARED are blocked until decision known.

## 涉及概念

- `failure recovery`
- `blocking`
- `write-ahead log`

## 实现提示

- 日志 before sending 消息
- Recovery reads 日志 state
- Participants query coordinator用于decision

## 测试用例

### 1. 日志 事务 state before prepare

Coordinator writes decision to durable 日志 (with fsync) BEFORE sending PREPARE/COMMIT/ABORT to participants

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
