# 添加 Request 去重

英文标题：Add Request Deduplication
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-12-2-dedup>

课程：12. 代理
任务序号：2
短标题：去重
难度：intermediate
子主题：Caching 代理

## 中文导读

本题要求你完成 `添加 Request 去重`。

重点关注：`deduplication`、`idempotency`、`request coalescing`。

建议先按提示逐步实现：Track in-flight requests by key。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Deduplicate identical concurrent requests to reduce backend load:

1. Compute a 请求 key (e.g., hash of method + URL + body)
2. If a 请求，包含the same key is already in-flight, wait用于it
3. When the original completes, return the same 响应 to all waiters
4. After 响应, remove from in-flight set

This is especially valuable用于hot endpoints，包含many identical requests.

## 概念说明

### Request 去重

When many clients 请求 the same resource simultaneously, sending all requests to the backend wastes resources. Deduplication sends one 请求和shares the 响应, reducing backend load dramatically.

### Request Fingerprinting

The dedup key must uniquely identify functionally equivalent requests. For GET requests, URL is often sufficient. For POST, you may need to hash the body. Be careful，包含headers that affect 响应.

## 涉及概念

- `deduplication`
- `idempotency`
- `request coalescing`

## 实现提示

- Track in-flight requests by key
- Have duplicates wait用于original
- Return same 响应 to all waiters

## 测试用例

### 1. Deduplicate concurrent

Multiple clients send identical requests (same idempotency key) to 代理 concurrently. 代理 should recognize duplicates, send only ONE 请求 to backend,和return same 响应 to all clients. Track requests by idempotency key.

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
