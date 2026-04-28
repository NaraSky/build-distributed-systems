# 实现精确一次处理

英文标题：Implement Exactly-Once Processing
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-5-exactly-once>

课程：30. MapReducer：批处理与流处理
任务序号：10
短标题：精确一次处理
难度：高级
子主题：Stream Processing

## 中文导读

本题要求你实现精确一次处理（Exactly-Once Processing）语义。在分布式流处理中，系统出错后会重试，这就可能导致同一个事件被重复处理。精确一次处理通过三个机制来保证每个事件只影响输出一次：去重、检查点和事务性提交。这是流处理系统最强的正确性保证，也是工程上最难做到的。

## 题目说明

精确一次处理意味着每个事件对输出的影响恰好一次，即使系统在故障后重试了操作也是如此。它结合了三种机制：**去重**（跳过已经处理过的事件）、**检查点（Checkpoint）**（保存状态快照以便故障恢复时从断点继续）、以及**事务性输出**（原子性地提交结果，要么全部成功要么全部回滚）。

```
没有精确一次处理时：
  处理 "hello"  -> count=1
  （崩溃，重试）
  处理 "hello"  -> count=2  <- 错误！被重复计数了

有精确一次处理时（去重）：
  处理 "hello" (id=e1)  -> count=1，标记 e1 已处理
  （崩溃，重试）
  处理 "hello" (id=e1)  -> 跳过（e1 已处理过）-> count=1 仍然正确
```

你的节点需要处理四种消息类型：

```json
// 处理一个事件；如果 event_id 已经见过则跳过
{ "type": "process", "msg_id": 1,
  "event_id": "e1", "word": "hello" }
-> { "type": "processed", "in_reply_to": 1,
    "word": "hello", "count": 1, "was_duplicate": false }

// 将当前状态保存为一个命名的检查点
{ "type": "checkpoint", "msg_id": 2, "checkpoint_id": "cp1" }
-> { "type": "checkpoint_saved", "in_reply_to": 2, "checkpoint_id": "cp1" }

// 从检查点恢复状态
{ "type": "restore", "msg_id": 3, "checkpoint_id": "cp1" }
-> { "type": "restored", "in_reply_to": 3,
    "counts": {"hello": 1} }

// 原子性地提交待输出的结果
{ "type": "commit", "msg_id": 4 }
-> { "type": "committed", "in_reply_to": 4, "output_count": 1 }
```

## 概念说明

精确一次处理可以用银行转账来理解：你不希望同一笔转账被执行两次（多扣了钱），也不希望它完全不执行（钱没到账）。去重就像银行给每笔转账一个唯一编号，即使请求因为网络问题被重复发送，银行也能识别出"这笔已经处理过了，不再重复执行"。检查点就像在某个时刻给系统拍一张"快照"，万一系统崩溃了，可以从快照恢复到崩溃前的状态，而不用从头来过。事务性提交则保证结果要么完整地写出去，要么完全不写，不会出现写了一半的情况。

## 涉及概念

- `exactly-once`
- `idempotency`
- `deduplication`
- `checkpointing`
- `transactional commits`

## 实现提示

- 用一个集合记录已处理的事件标识，静默跳过重复事件
- 检查点保存当前的计数状态，以便故障恢复时从断点继续
- 恢复操作加载检查点并替换当前状态
- 提交操作将待输出的结果原子性地变为已提交状态；回滚则丢弃这些结果
- 至少一次投递加上幂等性，等效于精确一次处理

## 测试用例

### 1. 幂等处理

相同事件标识的第二条消息不应产生任何效果（计数保持为 1）。

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"event_id":"e1","word":"hello"}}
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":2,"event_id":"e1","word":"hello"}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "word": "hello", "count": 1, "was_duplicate": false}
{"type": "processed", "in_reply_to": 2, "word": "hello", "count": 1, "was_duplicate": true}
```

### 2. 检查点与恢复

恢复操作应返回检查点保存时的状态。

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"event_id":"e1","word":"hello"}}
{"src":"client","dest":"processor","body":{"type":"checkpoint","msg_id":2,"checkpoint_id":"cp1"}}
{"src":"client","dest":"processor","body":{"type":"restore","msg_id":3,"checkpoint_id":"cp1"}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "word": "hello", "count": 1, "was_duplicate": false}
{"type": "checkpoint_saved", "in_reply_to": 2, "checkpoint_id": "cp1"}
{"type": "restored", "in_reply_to": 3, "counts": {"hello": 1}}
```

## 参考资料

- [Exactly-Once Semantics in Apache Kafka](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)：Kafka 如何实现端到端的精确一次投递

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
