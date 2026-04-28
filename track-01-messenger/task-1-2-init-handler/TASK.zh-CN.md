#处理初始化 消息和存储集群元数据

英文标题：Handle Init Message和Store集群元数据
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-init-handler>

课程：1. 信使：消息通信基础
任务序号：2
短标题：初始化 处理器
难度：beginner
子主题：Hello, Distributed World

## 中文导读

本题要求你完成 `Handle 初始化 消息和存储集群元数据`。

重点关注：`initialization`、`node identity`、`cluster topology`。

建议先按提示逐步实现：The init 消息 contains node_id和node_ids fields。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Before processing any workload, Maelstrom sends an init 消息 to each 节点. This 消息 tells your 节点 its identity和the full 集群 membership.

The init 消息 looks like:

```JSON
{
  "type": "init",
  "msg_id": 1,
  "node_id": "n1",
  "node_ids": ["n1", "n2", "n3"]
}
```

Your task is to handle the init 消息 by storing the node_id (your identity)和node_ids (all 集群 members). Then respond，包含an init_ok 消息:

```JSON
{
  "type": "init_ok",
  "in_reply_to": 1
}
```

The in_reply_to field must match the msg_id from the init 请求.

## 概念说明

##节点Initialization

Every distributed system needs a **bootstrap phase** where 节点 learn about themselves和their peers. The init 消息 serves this purpose in Maelstrom.

### Understanding Identity

The `node_id` field gives your 节点 its **unique identity**. This is critical because:

  - All 消息 you send must use this as the `src` field

  - Other 节点 will address 消息 to you使用this ID

  - Your identity distinguishes you from other 节点 in the 集群

### Cluster Topology

The `node_ids` array tells you about **all 节点 in the 集群**. This information becomes essential for:

  - **广播 algorithms** - knowing who to send 消息 to

  - **共识 protocols** - calculating quorums

  - **Leader election** - participating in voting

### Request-Response Pattern

The `in_reply_to` field establishes a **correlation** between requests和responses. This pattern is fundamental in 分布式系统 where you need to match responses to outstanding requests.

```text
Request:  { "type": "init", "msg_id": 1, ... }
Response: { "type": "init_ok", "in_reply_to": 1 }
```

This correlation allows the sender to:

  - Track which requests have been answered

  - Implement timeouts用于unresponsive 节点

  -处理out-of-order 消息 delivery

## 涉及概念

- `initialization`
- `node identity`
- `cluster topology`

## 实现提示

- The init 消息 contains node_id和node_ids fields
- Store these values用于use in subsequent 消息 handling
- Reply，包含init_ok 消息 type

## 测试用例

### 1. Respond to 初始化

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Maelstrom Initialization](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md#initialization)：Details on the init 消息和expected 响应

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
