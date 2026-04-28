# 实现 Collapsed Forwarding

英文标题：Implement Collapsed Forwarding
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-12-3-collapsed>

课程：12. 代理
任务序号：3
短标题：Collapsed Forwarding
难度：intermediate
子主题：Caching 代理

## 中文导读

本题要求你完成 `实现 Collapsed Forwarding`。

重点关注：`collapsed forwarding`、`thundering herd`、`cache miss handling`。

建议先按提示逐步实现：Similar to deduplication but用于缓存 misses。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement collapsed forwarding用于缓存 misses to prevent thundering herd:

When a cached item expires和multiple requests arrive:
1. First 请求 goes to the origin (is "collapsed")
2. Subsequent requests用于the same key wait
3. When origin responds, 缓存 the 响应
4. Return the cached 响应 to all waiting requests

This prevents the backend from being overwhelmed when popular items expire.

## 概念说明

### Thundering Herd Problem

When a popular cached item expires, thousands of requests might simultaneously miss the 缓存和hit the backend. This can overwhelm the backend和cause cascading failures.

### Collapsed Forwarding

Collapsed forwarding allows only one 请求 through to the origin while others wait. When the 响应 arrives, it is cached和returned to all waiters. CDNs like Varnish implement this.

## 涉及概念

- `collapsed forwarding`
- `thundering herd`
- `cache miss handling`

## 实现提示

- Similar to deduplication but用于缓存 misses
- Only one 请求 goes to origin
- 队列 waiters until 响应 arrives

## 测试用例

### 1. Collapse concurrent requests

缓存 miss用于key "x". Three concurrent requests用于key "x" arrive at 代理 simultaneously. First 请求 goes to backend (collapsed), other 2 wait. When backend responds, all 3 clients get the cached 响应. Verify only 1 backend call made.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [Varnish Collapsed Forwarding](https://varnish-cache.org/docs/)：Varnish documentation on 请求 coalescing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
