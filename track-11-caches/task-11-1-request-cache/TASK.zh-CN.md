# 实现 Request节点缓存

英文标题：Implement Request节点Cache
网页：<https://builddistributedsystem.com/tracks/caches/tasks/task-11-1-request-cache>

课程：11. 缓存
任务序号：1
短标题：Request 缓存
难度：intermediate

## 中文导读

本题要求你完成 `实现 Request节点缓存`。

重点关注：`caching`、`local cache`、`TTL`。

建议先按提示逐步实现：缓存 responses at the 请求 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a local 缓存 at each 请求-handling 节点. When a 请求 comes in:

1. Check if the key exists in the local 缓存
2. If 缓存 hit和not expired, return cached value
3. If 缓存 miss or expired, fetch from backend
4. Store result in 缓存，包含TTL
5. Return result

Track 缓存 hit rate to measure effectiveness.

## 概念说明

### Why Caching?

Caching trades space用于time. By storing frequently accessed data closer to the requester, we reduce latency和backend load. A 缓存，包含90% hit rate reduces backend traffic by 10x.

### Request节点缓存

The simplest 缓存 sits at each 请求 handler. It is fast (no 网络 hop) but duplicates data across 节点. This works well用于hot data that all 节点 access.

### TTL (Time-To-Live)

TTL defines how long cached data remains valid. Short TTL = more freshness, more backend load. Long TTL = less freshness, less load. Choose based on how often data changes和tolerance用于staleness.

## 涉及概念

- `caching`
- `local cache`
- `TTL`

## 实现提示

- 缓存 responses at the 请求 节点
- Use TTL用于freshness control
- Check 缓存 before calling backend

## 测试用例

### 1. 缓存 hit

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"cache_write","msg_id":2,"key":"x","value":100}}
{"src":"c2","dest":"n1","body":{"type":"cache_read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"cache_write_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"cache_read_ok","in_reply_to":3,"msg_id":2,"hit":true,"value":100}}
```

## 参考资料

- [Caching Strategies](https://aws.amazon.com/caching/)：AWS guide to caching strategies
- [DDIA Chapter 5](https://dataintensive.net/)：复制和caching concepts

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
