# 构建 Reverse 代理，包含Caching

英文标题：Build Reverse Proxy，包含Caching
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-12-4-reverse-proxy>

课程：12. 代理
任务序号：4
短标题：Reverse 代理
难度：intermediate
子主题：Caching 代理

## 中文导读

本题要求你完成 `构建 Reverse 代理，包含Caching`。

重点关注：`reverse proxy`、`HTTP caching`、`Cache-Control`。

建议先按提示逐步实现：Parse HTTP headers用于caching hints。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build an HTTP-aware reverse 代理，包含caching:

1. Parse incoming HTTP requests
2. Check 缓存用于valid 响应
3. On 缓存 miss, forward to backend
4. Parse 响应 headers用于caching policy
5. 缓存 响应 according to 缓存-Control
6. Return 响应 to 客户端

Support ETag和If-Modified-Since用于缓存 validation.

## 概念说明

### HTTP Caching Headers

HTTP provides rich 缓存 control: 缓存-Control sets freshness duration, ETag enables validation without full fetch, Vary handles content negotiation. A good 代理 respects all of these.

### 缓存 校验

Instead of fetching a full 响应, validation asks "has this changed?"使用If-None-Match (with ETag) or If-Modified-Since. A 304 Not Modified 响应 confirms the cached copy is still valid.

## 涉及概念

- `reverse proxy`
- `HTTP caching`
- `Cache-Control`

## 实现提示

- Parse HTTP headers用于caching hints
- Honor 缓存-Control directives
- Implement ETag validation

## 测试用例

### 1. 缓存，包含max-age

Backend responds，包含缓存-Control: max-age=60. Reverse 代理 should 缓存 响应用于60 seconds. Requests within 60s should return cached 响应 without hitting backend. After 60s, 缓存 expires和代理 should fetch fresh 响应.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Honor no-存储

Backend responds，包含缓存-Control: no-store. Reverse 代理 should NOT 缓存 this 响应. Every 请求 should go to backend, even用于same URL. Verify 代理 respects no-store directive.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)：MDN guide to HTTP caching

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
