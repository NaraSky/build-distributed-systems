# 实现 Compare-And-Swap (CAS) Operation

英文标题：Implement Compare-And-Swap (CAS) Operation
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-3-cas-operation>

课程：4. 计数器：分布式状态与 CRDT
任务序号：3
短标题：Compare-And-Swap
难度：intermediate
子主题：The Lost Update Problem

## 中文导读

本题要求你完成 `实现 Compare-And-Swap (CAS) Operation`。

重点关注：`CAS`、`optimistic concurrency`、`atomic operations`。

建议先按提示逐步实现：Read current value, compute new, CAS to update。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement your 计数器使用Compare-And-Swap (CAS) operations. CAS atomically updates a value only if it matches an expected value, preventing lost updates.

## 概念说明

### Compare-And-Swap

CAS is the foundation of lock-free algorithms. It atomically checks if a value equals an expected value and, if so, updates it. If the check fails, someone else modified the value和you must 重试.

## 涉及概念

- `CAS`
- `optimistic concurrency`
- `atomic operations`

## 实现提示

- Read current value, compute new, CAS to update
- 重试 on CAS 故障
-处理the race between read和CAS

## 测试用例

### 1. CAS-based 计数器

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":5}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":5}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
