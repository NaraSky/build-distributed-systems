# 构建带缓存的反向代理

英文标题：Build Reverse Proxy with Caching
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-12-4-reverse-proxy>

课程：12. 代理
任务序号：4
短标题：反向代理
难度：进阶
子主题：缓存代理

## 中文导读

这道题要求你构建一个能理解 HTTP 协议的反向代理，并实现缓存功能。反向代理位于后端服务器前面，接收客户端请求并根据缓存策略决定是返回缓存内容还是转发给后端。理解 HTTP 缓存机制是构建高性能 Web 系统的核心技能之一。

## 题目说明

构建一个支持缓存的 HTTP 反向代理：

1. 解析客户端发来的 HTTP 请求
2. 检查缓存中是否有有效的响应
3. 如果缓存未命中，将请求转发给后端
4. 解析响应头中的缓存策略
5. 根据 Cache-Control 头的指示缓存响应
6. 将响应返回给客户端

需要支持 ETag 和 If-Modified-Since 两种缓存验证机制。

## 概念说明

### HTTP 缓存头

HTTP 协议提供了丰富的缓存控制机制：Cache-Control 用于设置缓存的有效时长，ETag 可以在不获取完整内容的情况下验证缓存是否仍然有效，Vary 头用于处理内容协商。一个好的代理应该遵守所有这些缓存指令。

### 缓存验证

缓存验证不需要获取完整的响应内容，而是询问"这个资源是否已经改变了？"。具体做法是通过 If-None-Match（配合 ETag）或 If-Modified-Since 头来实现。如果服务端返回 304 Not Modified 状态码，就说明缓存中的副本仍然是最新的，可以直接使用。

## 涉及概念

- `reverse proxy`
- `HTTP caching`
- `Cache-Control`

## 实现提示

- 解析 HTTP 头部中的缓存相关信息
- 遵守 Cache-Control 指令
- 实现 ETag 验证机制

## 测试用例

### 1. 使用 max-age 缓存

后端响应包含 Cache-Control: max-age=60。反向代理应将响应缓存 60 秒。在 60 秒内的请求应直接返回缓存内容，不需要访问后端。60 秒过后，缓存过期，代理应重新从后端获取最新响应。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. 遵守 no-store 指令

后端响应包含 Cache-Control: no-store。反向代理不应缓存此响应。即使是对同一个 URL 的请求，每次都必须转发给后端。验证代理确实遵守了 no-store 指令。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)：MDN 上的 HTTP 缓存指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
