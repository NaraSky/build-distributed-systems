# 实现 基础 计数器，包含Lost Update Problem

英文标题：Implement Basic Counter，包含Lost Update Problem
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-1-lost-update>

课程：4. 计数器：分布式状态与 CRDT
任务序号：1
短标题：Lost Updates
难度：beginner
子主题：The Lost Update Problem

## 中文导读

本题要求你完成 `实现 基础 计数器，包含Lost Update Problem`。

重点关注：`lost updates`、`race conditions`、`naive replication`。

建议先按提示逐步实现：Start，包含a simple 计数器。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a basic grow-only 计数器 that handles add和read operations. Multiple 节点 share 计数器 state, but your initial implementation will lose updates under concurrency.

This task intentionally demonstrates the lost update problem. Your 计数器 will work用于sequential operations but fail verification under concurrent updates from multiple 节点.

## 概念说明

### The Lost Update Problem

When multiple 节点 read, modify,和write state, updates can be lost. 节点 A reads 5, 节点 B reads 5, both increment to 6, both write 6. One increment is lost. This is why distributed counters need special handling.

## 涉及概念

- `lost updates`
- `race conditions`
- `naive replication`

## 实现提示

- Start，包含a simple 计数器
- Notice what happens，包含concurrent updates
- This task is meant to fail

## 测试用例

### 1. 基础 计数器 添加

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":5}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":5}}
```

### 2. Sequential increments work

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":3}}
{"src":"c2","dest":"n1","body":{"type":"add","msg_id":3,"delta":2}}
{"src":"c3","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"add_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c3","body":{"type":"read_ok","in_reply_to":4,"msg_id":3,"value":5}}
```

## 参考资料

- [G-Counter Challenge](https://fly.io/dist-sys/4/)：Fly.io grow-only 计数器 challenge

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
