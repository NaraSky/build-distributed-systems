# 构建 Layer 7 Load Balancer

英文标题：Build Layer 7 Load Balancer
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-4-layer7>

课程：14. 负载均衡器
任务序号：4
短标题：Layer 7 LB
难度：intermediate
子主题：Layer 4 Load Balancing

## 中文导读

本题要求你完成 `构建 Layer 7 Load Balancer`。

重点关注：`Layer 7`、`HTTP routing`、`content-based`。

建议先按提示逐步实现：Parse HTTP headers。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build an HTTP-aware (Layer 7) load balancer:

1. Parse HTTP 请求 (method, path, headers)
2. Route based on Host header (virtual hosts)
3. Route based on URL path (/api/* -> api-servers)
4. Implement session stickiness via cookie
5. Support URL rewriting

Layer 7 enables intelligent routing based on 请求 content.

## 概念说明

### Layer 4 vs Layer 7

Layer 4 LBs see only TCP/UDP - fast but limited. Layer 7 LBs understand HTTP - can route by URL, read cookies, modify headers. More powerful but higher overhead.

### Session Stickiness

Some apps require all requests from a user to reach the same 服务端 (sessions). The LB can track sessions via cookies or source IP. Trade-off: stickiness can cause uneven load.

## 涉及概念

- `Layer 7`
- `HTTP routing`
- `content-based`

## 实现提示

- Parse HTTP headers
- Route based on path or host
- Support session stickiness

## 测试用例

### 1. Path-based routing

Layer 7 LB，包含path-based rules: /api/* -> [s1, s2], /web/* -> [s3]. 请求用于/api/users routes to s1 or s2.

输入：

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"path":"/api/users","method":"GET"}}
```

期望输出：

```text
{"src":"lb","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"lb","dest":"client","body":{"type":"http_response","in_reply_to":2,"msg_id":1,"path":"/api/users","routed_to":"s1","status":200}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
