# 实现 Consistent Hashing用于Load Balancing

英文标题：Implement Consistent Hashing用于Load Balancing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-5-consistent-hashing-lb>

课程：14. 负载均衡器
任务序号：5
短标题：Consistent Hash LB
难度：advanced
子主题：Layer 4 Load Balancing

## 中文导读

本题要求你完成 `实现 Consistent Hashing用于Load Balancing`。

重点关注：`consistent hashing`、`key affinity`、`cache locality`。

建议先按提示逐步实现：Hash 请求 key to 服务端。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement consistent hashing用于stateful load balancing:

1. Assign servers to positions on hash ring
2. Hash each 请求 key to ring position
3. Route to 服务端 clockwise from hash position
4. When servers join/leave, only nearby keys move

This maintains 缓存 locality - same user always hits same 服务端, maximizing 缓存 hits.

## 概念说明

### Consistent Hashing用于LB

For stateful services or caching, you want related requests to hit the same 服务端. Consistent hashing routes based on a key (user ID, session), ensuring same key -> same 服务端 while minimizing redistribution.

### Virtual Nodes

With few servers, distribution can be uneven. Virtual 节点 map each 服务端 to many ring positions, smoothing the distribution.

## 涉及概念

- `consistent hashing`
- `key affinity`
- `cache locality`

## 实现提示

- Hash 请求 key to 服务端
- Same key always goes to same 服务端
- Minimal redistribution on 服务端 changes

## 测试用例

### 1. Consistent routing

Load balancer uses consistent hashing，包含3 servers (s1, s2, s3). 请求，包含key "user123" routes to s2. Subsequent requests，包含same key "user123" should always route to s2. Verify consistent routing based on 请求 key.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Minimal redistribution

Load balancer，包含3 servers handling 1000 keys. Add 4th 服务端 s4. With consistent hashing, only ~250 keys (1000/4) should remap to s4. Other keys stay on original servers. Verify adding 节点 causes minimal redistribution compared to modulo hashing.

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
