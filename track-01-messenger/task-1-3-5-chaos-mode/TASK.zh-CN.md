# 添加混沌模式：随机丢弃消息

英文标题：Add Chaos Mode with Random Message Dropping
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-5-chaos-mode>

课程：1. 信使：消息通信基础
任务序号：15
短标题：混沌模式
难度：进阶
子主题：协议底层机制

## 中文导读

真实的网络会丢消息。Netflix 开创了**混沌工程（Chaos Engineering）**的方法论——故意注入故障来测试系统的抗压能力。这道题要求你给节点添加一个"混沌模式"，开启后会按一定概率随机丢弃发出的消息，模拟网络丢包。

混沌工程是验证分布式系统可靠性的重要手段。与其等到生产环境出故障才发现问题，不如主动注入故障来提前暴露薄弱环节。

## 题目说明

真实的网络会丢消息——这不是"万一发生"，而是"一定会发生"。Netflix 率先提出了**混沌工程**的理念：与其被动等待故障发生，不如主动注入故障来测试系统的韧性。

你的任务是给节点添加"混沌模式"。开启混沌模式后，节点会按照可配置的概率随机丢弃**发出的**消息（不写入标准输出），以此模拟网络丢包的场景。

需要实现以下消息类型：

1. `chaos_on` —— 以指定的丢弃率开启混沌模式：

```json
Request:  {"type": "chaos_on", "msg_id": 1, "drop_rate": 0.1}
Response: {"type": "chaos_on_ok", "in_reply_to": 1, "drop_rate": 0.1}
```

2. `chaos_off` —— 关闭混沌模式：

```json
Request:  {"type": "chaos_off", "msg_id": 2}
Response: {"type": "chaos_off_ok", "in_reply_to": 2}
```

3. `chaos_stats` —— 报告混沌模式的统计信息：

```json
Request:  {"type": "chaos_stats", "msg_id": 3}
Response: {"type": "chaos_stats_ok", "in_reply_to": 3, "enabled": true, "drop_rate": 0.1, "total_sent": 50, "total_dropped": 5}
```

为了在测试中保证可复现性，请使用固定的随机数种子（42）。丢弃的判断逻辑是 `random.nextDouble() < drop_rate`。

混沌模式**不能丢弃控制消息**（`init_ok`、`chaos_on_ok`、`chaos_off_ok`、`chaos_stats_ok`），只丢弃应用消息（如 `echo_ok`）。

## 概念说明

### 什么是混沌工程

打个比方：消防演习不是因为真的着火了，而是为了提前发现逃生通道是否畅通、灭火器是否能用。混沌工程也是同样的道理——在可控的环境下主动制造故障，观察系统是否能正确应对。

Netflix 的 Chaos Monkey 是最著名的混沌工程工具，它会随机杀死生产环境中的服务实例，迫使工程师必须把系统设计成能容忍任意节点失败。

### 为什么只丢弃发出的消息

在真实网络中，丢包发生在传输过程中，也就是消息已经从发送方出去了，但没到达接收方。模拟时我们在发送环节做拦截——让节点"以为"自己发了消息，但实际上没有写入标准输出。这样就模拟了消息在网络传输中丢失的效果。

### 为什么不丢弃控制消息

控制消息（如 `init_ok`、`chaos_on_ok`）是管理混沌模式本身的命令。如果连这些消息也丢了，你就无法控制混沌模式的开关了——这就像把灭火器也扔进火里一样。

## 涉及概念

- `chaos engineering`
- `fault injection`
- `resilience testing`
- `network partitions`

## 实现提示

- 使用随机数生成器来决定是否丢弃每条发出的消息
- 丢弃率应该可配置（默认 10%）
- 将被丢弃的消息信息输出到标准错误（stderr），方便观察混沌效果
- 跟踪已发送和已丢弃的消息数量
- 混沌模式应该可以通过消息动态开关

## 测试用例

### 1. 未开启混沌模式时初始化和回声正常工作

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"safe"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "safe", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 开启混沌模式后返回丢弃率

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chaos_on","msg_id":2,"drop_rate":0.5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "chaos_on_ok", "drop_rate": 0.5, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Principles of Chaos Engineering](https://principlesofchaos.org/)：混沌工程方法论的奠基性文档
- [Netflix Chaos Monkey](https://netflix.github.io/chaosmonkey/)：Netflix 开源的混沌工程工具，用于在生产环境中随机终止服务实例

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
