# 处理初始化消息并存储集群元数据

英文标题：Handle Init Message and Store Cluster Metadata
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-init-handler>

课程：1. 信使：消息通信基础
任务序号：2
短标题：初始化处理器
难度：入门
子主题：Hello, Distributed World

## 中文导读

在 Maelstrom 开始发送真正的工作负载之前，它会先给每个节点发一条初始化消息，告诉你"你是谁"以及"集群里还有谁"。你的任务就是正确处理这条消息，把自己的身份和集群成员信息存下来，然后回复一条确认。

这是构建分布式节点的第一步——每个节点必须先知道自己的身份，才能正确地收发消息。

## 题目说明

在处理任何工作负载之前，Maelstrom 会向每个节点（Node）发送一条 `init` 类型的初始化消息。这条消息会告诉你的节点两件事：你的节点编号（`node_id`）和集群中所有节点的列表（`node_ids`）。

初始化消息的格式如下：

```json
{
  "type": "init",
  "msg_id": 1,
  "node_id": "n1",
  "node_ids": ["n1", "n2", "n3"]
}
```

你需要做的是：
1. 从消息中读取 `node_id`（你自己的身份标识）和 `node_ids`（集群所有成员），保存起来
2. 回复一条 `init_ok` 消息，表示初始化完成

回复消息的格式如下：

```json
{
  "type": "init_ok",
  "in_reply_to": 1
}
```

注意：`in_reply_to` 字段的值必须和收到的 `init` 消息中的 `msg_id` 一致，用来表明"这是对哪条请求的回复"。

## 概念说明

### 节点初始化

每个分布式系统都需要一个**引导阶段（Bootstrap Phase）**，让各节点了解自己是谁、集群里还有哪些伙伴。在 Maelstrom 中，`init` 消息就承担了这个角色。

打个比方：你加入一个新团队，第一天上班时 HR 会告诉你"你的工号是 n1"，还会给你一份团队花名册。`init` 消息做的就是这件事。

### 节点身份

`node_id` 字段赋予了你的节点一个**唯一身份**。这非常关键，因为：

- 你发送的所有消息都必须把它作为 `src`（发送者）字段
- 其他节点会用这个编号给你发消息
- 它是你在集群中区别于其他节点的唯一标识

### 集群拓扑

`node_ids` 数组告诉你**集群中所有节点的列表**。这个信息在后续的很多场景中都会用到：

- **广播算法** —— 知道要把消息发给谁
- **共识协议** —— 计算多数派（Quorum）
- **领导者选举** —— 参与投票

### 请求-响应模式

`in_reply_to` 字段建立了请求和响应之间的**关联关系**。这种模式在分布式系统中非常基础——你需要知道"这条回复是针对哪条请求的"。

```text
Request:  { "type": "init", "msg_id": 1, ... }
Response: { "type": "init_ok", "in_reply_to": 1 }
```

通过这种关联机制，发送方可以：

- 追踪哪些请求已经被响应
- 对未响应的节点设置超时
- 处理消息的乱序到达

## 涉及概念

- `initialization`
- `node identity`
- `cluster topology`

## 实现提示

- 初始化消息的 `body` 中包含 `node_id` 和 `node_ids` 两个字段
- 把这两个值保存下来，后续处理消息时会用到
- 回复消息的类型是 `init_ok`

## 测试用例

### 1. 响应初始化消息

收到 `init` 消息后，正确保存节点身份，并回复 `init_ok`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Maelstrom Initialization](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md#initialization)：Maelstrom 初始化消息的官方文档，描述了 init 消息的格式和预期响应

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
