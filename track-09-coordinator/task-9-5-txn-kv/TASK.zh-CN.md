# 构建事务型键值存储

英文标题：Build Transactional Key-Value Store
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-5-txn-kv>

课程：9. 协调器：分布式事务
任务序号：5
短标题：Txn KV
难度：高级
子主题：Two-Phase Commit

## 中文导读

本题要求你构建一个支持事务的分布式键值存储。你需要实现开始事务、读取、写入、提交和中止等操作，并使用两阶段提交来处理跨分片的事务。这是将前面学到的两阶段提交知识应用到实际存储系统中的综合练习。

## 题目说明

实现一个事务型键值存储，支持以下操作：开始事务（begin）、读取（read）、写入（write）、提交（commit）和中止（abort）。对于涉及多个分片（Shard）的事务，使用两阶段提交来保证原子性。

## 概念说明

### ACID 特性

ACID 是事务的四个核心特性：原子性（Atomic）、一致性（Consistent）、隔离性（Isolated）、持久性（Durable）。在分布式环境下，由于网络分区（Network Partition）的存在，实现事务要比单机困难得多。

## 涉及概念

- `transactions`
- `ACID`
- `isolation`

## 实现提示

- 支持多键事务
- 跨分片事务使用两阶段提交
- 实现"读己之写"语义，确保事务内能读到自己刚写入的数据

## 测试用例

### 1. 开始事务

响应应包含 txn_begin_ok 和一个唯一的事务标识。事务应处于活跃状态。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"txn_begin","msg_id":2}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"txn_begin_ok","in_reply_to":2,"msg_id":1,"tx_id":"tx1"}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
