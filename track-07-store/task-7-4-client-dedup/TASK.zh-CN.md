#处理Client 重试和去重

英文标题：Handle Client Retry和Deduplication
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-7-4-client-dedup>

课程：7. 存储：线性一致 KV Store
任务序号：4
短标题：Client Dedup
难度：intermediate
子主题：Linearizable 键值 存储

## 中文导读

本题要求你完成 `Handle Client 重试和去重`。

重点关注：`idempotency`、`client sessions`、`deduplication`。

建议先按提示逐步实现：客户端 assigns unique ID to each 请求。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Handle 客户端 retries without duplicate execution:

1. 客户端 assigns sequence number to each 请求
2. 服务端 tracks (client_id -> latest_seq, 响应)
3. If 请求 seq <= latest_seq, return cached 响应
4. Otherwise, process和缓存 new 响应

This makes at-least-once delivery safe用于non-idempotent operations.

## 概念说明

### Exactly-Once Semantics

网络 issues cause retries. Without deduplication, a PUT might execute twice. By tracking 客户端 sessions和sequence numbers, we can detect和skip duplicates.

### Session State

The deduplication table must survive Leader changes. Store it in the replicated state machine. Periodically garbage collect old sessions.

## 涉及概念

- `idempotency`
- `client sessions`
- `deduplication`

## 实现提示

- 客户端 assigns unique ID to each 请求
- 服务端 tracks latest 响应 per 客户端
- Duplicate 请求 returns cached 响应

## 测试用例

### 1. First request executes

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"write","msg_id":2,"key":"x","value":1,"client_id":"c1","seq":1}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"write_ok","in_reply_to":2,"msg_id":1}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
