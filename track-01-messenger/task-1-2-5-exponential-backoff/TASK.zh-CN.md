# 实现指数退避重试机制

英文标题：Implement Exponential Backoff for Retries
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-5-exponential-backoff>

课程：1. 信使：消息通信基础
任务序号：10
短标题：指数退避
难度：进阶
子主题：RPC 与请求-响应模型

## 中文导读

当 RPC 请求失败时，最简单的做法是立刻重试。但如果所有节点都以固定间隔重试，就会形成"惊群效应"，让本来就在恢复中的系统雪上加霜。这道题要求你实现指数退避（Exponential Backoff）策略——每次重试的等待时间翻倍，并加入随机抖动。

指数退避是分布式系统和网络编程中最常见的重试策略，从 TCP 协议到云服务 SDK 都在用它。掌握这个模式，你就能写出更"懂事"的客户端程序。

## 题目说明

在分布式系统中，当请求失败需要重试时，如果所有节点都以固定间隔（比如每秒重试一次）发起重试，就会造成**惊群效应（Thundering Herd）**——大量请求同时涌向刚恢复的服务，反而阻碍了它的恢复。

**指数退避**的核心思想很简单：每次重试，等待时间翻倍。打个比方：你给朋友打电话没人接，第一次等 1 分钟再打，第二次等 2 分钟，第三次等 4 分钟……这样既给了对方恢复的时间，又避免了频繁骚扰。

你的任务是实现 `rpc_with_backoff` 方法，具体规则如下：

1. 第一次重试前等待 `base_delay`（默认 100 毫秒）
2. 每次重试后等待时间翻倍：`delay = base_delay * 2^attempt`
3. 加入随机抖动（Jitter）：`delay += random(0, delay * 0.1)`，避免多个节点同步重试
4. 等待时间不超过 `max_delay`（默认 2 秒）上限
5. 最多重试 `max_retries` 次（默认 5 次）后放弃

需要实现 `backoff_relay` 消息类型：

```json
Request:  {"type": "backoff_relay", "msg_id": 1, "target": "n2", "payload": {"type": "read"}}
Response: {"type": "backoff_relay_ok", "in_reply_to": 1, "attempts": 3, "total_delay_ms": 700}
```

响应中包含重试次数和总等待时间（毫秒）。本题的重点是退避计算逻辑，你的节点应该输出计算出的等待时间表。

另外，请在代码中写一段注释（至少 100 个英文单词），解释为什么指数退避在高负载场景下有用。

## 概念说明

### 为什么固定间隔重试有问题

假设有 100 个客户端同时请求一个服务，服务暂时不可用。如果它们都每隔 1 秒重试一次，那么服务每秒都会收到 100 个请求的冲击。这就像 100 个人同时挤进一扇门——谁也过不去。

### 指数退避如何解决问题

使用指数退避后，各个客户端的重试时间会自然错开。第一个客户端可能在 100 毫秒后重试，第二个在 200 毫秒后，第三个在 400 毫秒后……再加上随机抖动，重试请求就会均匀分散在时间轴上，给服务留出喘息和恢复的空间。

### 随机抖动的作用

即使使用了指数退避，如果所有客户端在同一时刻开始计时，它们的重试时间仍然是同步的（都在 100ms、200ms、400ms 重试）。加入随机抖动后，每个客户端的等待时间都有一点随机偏移，彻底打破了同步。

## 涉及概念

- `exponential backoff`
- `jitter`
- `congestion control`
- `load management`

## 实现提示

- 基础延迟每次翻倍：`delay = base_delay * 2^attempt`
- 加入随机抖动防止惊群效应：`delay += random(0, delay * 0.5)`
- 设置最大延迟上限，避免等待时间过长
- 记录每次重试的计算延迟，方便观察和调试
- 总等待时间是所有延迟之和，不只是最后一次的延迟

## 测试用例

### 1. 初始化和回声功能正常

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"backoff"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "backoff", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 计算退避时间表

节点应该返回 `compute_backoff_ok`，包含 `schedule_ms` 数组、`total_ms` 和 `retries` 字段。由于随机抖动的存在，具体数值会有变化，但响应结构必须正确。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compute_backoff","msg_id":2,"max_retries":3,"base_delay":0.1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)：AWS 架构博客关于退避策略的详细分析
- [TCP Congestion Control](https://en.wikipedia.org/wiki/TCP_congestion_control)：TCP 协议如何使用指数退避进行拥塞控制

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
