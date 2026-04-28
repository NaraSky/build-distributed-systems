# Ensure Read Consistency

英文标题：Ensure Read Consistency
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-7-3-read-consistency>

课程：7. 存储：线性一致 KV Store
任务序号：3
短标题：Read Consistency
难度：advanced
子主题：Linearizable 键值 存储

## 中文导读

本题要求你完成 `Ensure Read Consistency`。

重点关注：`linearizable reads`、`read index`、`lease`。

建议先按提示逐步实现：Simple: reads also go through 日志。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement 线性一致 reads:

Option 1: 日志 reads (simple but slow)
- Treat reads as 日志 entries, wait用于commit

Option 2: ReadIndex (Raft optimization)
- Record current commit 索引
- Confirm still Leader (心跳 round)
- Wait用于commit 索引 to be applied
- Execute read

Option 3: Lease (fast but 时钟-dependent)

## 概念说明

### The Stale Read Problem

A Leader might be partitioned和not know it. If it serves reads from local state, it returns stale data. Linearizability requires that reads reflect all prior writes.

### ReadIndex

Before serving a read, confirm you are still Leader by getting acknowledgment from a majority. Then wait用于the commit 索引 at that moment to be applied. This ensures linearizability without logging reads.

## 涉及概念

- `linearizable reads`
- `read index`
- `lease`

## 实现提示

- Simple: reads also go through 日志
- Optimized: confirm leadership before read
- Lease-based: use time bounds

## 测试用例

### 1. Read via 日志 is linearizable

Multi-节点 test: Write x=1, commit, then read x. Verify read returns 1和only returns after write is committed (linearizability).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [Raft Section 8](https://raft.github.io/raft.pdf)：客户端 interaction in Raft

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
