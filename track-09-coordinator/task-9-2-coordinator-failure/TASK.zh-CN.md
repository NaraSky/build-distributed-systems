# 处理协调者故障

英文标题：Handle Coordinator Failure
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-2-coordinator-failure>

课程：9. 协调器：分布式事务
任务序号：2
短标题：Coordinator Failure
难度：高级
子主题：Two-Phase Commit

## 中文导读

本题要求你处理两阶段提交中协调者崩溃的情况。在分布式系统中，协调者随时可能宕机，你需要通过预写日志来保证协调者重启后能正确恢复，继续完成或中止事务。这是理解分布式系统容错机制的核心练习。

## 题目说明

处理协调者故障：在发送 PREPARE 之前先写日志，在做出 COMMIT 或 ABORT 决策时也先写日志，然后再发送消息。协调者崩溃重启后，通过读取日志恢复到之前的状态，继续完成未完成的事务。

## 概念说明

### 预写日志

预写日志（Write-Ahead Logging）的核心思想是：先写日志，再发消息。协调者在发送任何消息之前，先把决策持久化到磁盘。恢复时，读取日志就能知道之前进行到了哪一步。在此期间，那些已经处于 PREPARED 状态的参与者会被阻塞，直到获知最终决策。

## 涉及概念

- `failure recovery`
- `blocking`
- `write-ahead log`

## 实现提示

- 在发送消息之前先写日志
- 恢复时读取日志，获取当前事务状态
- 参与者可以向协调者查询事务的最终决策

## 测试用例

### 1. 在准备阶段之前记录事务状态

协调者在发送 PREPARE、COMMIT 或 ABORT 给参与者之前，先将决策写入持久化日志（需要 fsync 确保落盘）。

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
