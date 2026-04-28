# 使用 LRU 缓存实现消息去重

英文标题：Implement Message Deduplication with LRU Cache
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-3-deduplication>

课程：1. 信使：消息通信基础
任务序号：13
短标题：消息去重
难度：进阶
子主题：协议底层机制

## 中文导读

网络可能会让消息"分身"。当发送方没收到确认就重试时，接收方可能会收到两条一模一样的请求。如果不做去重处理，同一个操作会被执行两次，导致状态错误。这道题要求你实现一个基于 LRU 缓存的消息去重机制。

消息去重是实现幂等性（Idempotency）的关键手段，几乎所有生产级别的分布式系统都需要它。

## 题目说明

网络可以复制消息。想象这样一个场景：节点 A 给节点 B 发了一条请求，B 收到并处理了，但回复的确认消息在网络中丢失了。A 没收到确认，以为请求失败了，于是重新发送。这时 B 就收到了两条完全相同的请求。如果不做**去重（Deduplication）**，B 就会把同一个请求处理两次，可能导致数据错误（比如余额被扣了两次）。

你的任务是实现消息去重机制：

1. 维护一个有界的 **LRU 缓存（Least Recently Used Cache）**，容量为 1000，保存最近处理过的消息 ID
2. 去重的键是 `(src, msg_id)` 这个组合——因为 `msg_id` 只在单个发送方内唯一，不同发送方可能使用相同的 `msg_id`
3. 检测到重复消息时，跳过业务处理，但仍然回复（确保发送方的重试能收到确认）
4. 跟踪并报告去重统计信息

需要实现 `dedup_echo` 消息类型，它的行为类似 `echo`，但会应用去重逻辑：

```json
Request:  {"type": "dedup_echo", "msg_id": 5, "echo": "hello"}
Response: {"type": "dedup_echo_ok", "in_reply_to": 5, "echo": "hello", "was_duplicate": false}
```

如果收到了相同的 `(src, msg_id)` 组合：

```json
Response: {"type": "dedup_echo_ok", "in_reply_to": 5, "echo": "hello", "was_duplicate": true}
```

还需要实现 `dedup_stats` 消息类型，用于查询去重统计：

```json
Response: {"type": "dedup_stats_ok", "total": 10, "duplicates": 2, "cache_size": 8}
```

## 概念说明

### 为什么需要去重

打个比方：你在网上购物，点了"付款"按钮后页面没反应，于是你又点了一次。如果系统没有去重机制，你可能会被扣两次款。消息去重就是为了解决这个问题——确保同一个操作不管发了几次，只被执行一次。

### LRU 缓存是什么

LRU 缓存是一种有固定容量的缓存，当缓存满了需要淘汰旧数据时，它会优先淘汰"最近最少使用"的条目。在本题中，我们用 LRU 缓存记录最近 1000 个已处理的消息 ID。新消息到来时，先查缓存——如果命中，说明是重复消息。

### 为什么去重键是 (src, msg_id)

`msg_id` 只在单个发送方范围内是唯一的。比如客户端 c1 和客户端 c2 可能同时发送 `msg_id = 5` 的消息，但它们是完全不同的请求。所以必须把发送方和消息 ID 组合起来作为去重键。

### 为什么重复消息也要回复

即使检测到重复，也必须回复。因为重复消息通常是由于发送方没收到上一次的确认而发起的重试。如果我们不回复，发送方会继续重试，造成更多不必要的流量。

## 涉及概念

- `idempotency`
- `deduplication`
- `LRU cache`
- `at-most-once delivery`

## 实现提示

- 使用 `(src, msg_id)` 作为去重键，因为 `msg_id` 只在单个发送方内唯一
- 在 Java 中可以使用 `LinkedHashMap` 配合 `removeEldestEntry` 来实现有界 LRU 缓存
- 当缓存超过容量时，删除最旧的条目
- 对重复消息跳过业务处理，但仍然回复确认
- 将重复消息的检测信息输出到标准错误，方便调试

## 测试用例

### 1. 第一次 dedup_echo 不是重复消息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"first"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "first", "was_duplicate": false, "in_reply_to": 10, "msg_id": 1}}
```

### 2. 来自同一来源的重复消息被检测到

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"hello"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "hello", "was_duplicate": false, "in_reply_to": 10, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "hello", "was_duplicate": true, "in_reply_to": 10, "msg_id": 2}}
```

## 参考资料

- [Exactly-Once Delivery in Distributed Systems](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)：Confluent 博客关于 Kafka 中去重和精确一次语义的介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
