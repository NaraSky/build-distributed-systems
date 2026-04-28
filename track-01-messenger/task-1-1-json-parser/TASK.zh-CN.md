# 实现基础 JSON 消息解析器

英文标题：Implement Basic JSON Message Parser
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-1-json-parser>

课程：1. 信使：消息通信基础
任务序号：1
短标题：JSON 解析器
难度：入门
子主题：Hello, Distributed World

## 中文导读

这是整个课程的第一道题。你要做的事情很简单：从标准输入（stdin）逐行读取 JSON 格式的消息，解析出发送者、接收者和消息类型，然后按指定格式输出。

这道题帮你建立分布式系统最基本的概念——节点之间通过消息通信。后续所有题目都建立在这个基础之上。

## 题目说明

在分布式系统中，各个节点（Node）无法共享内存，只能通过发送和接收消息来通信。本课程使用的 Maelstrom 测试框架采用 JSON 格式的消息，通过标准输入（stdin）和标准输出（stdout）进行通信。

你的任务是实现一个基础消息解析器：从标准输入逐行读取 JSON 消息，解析后将关键字段按指定格式输出到标准输出。

每条消息的 JSON 结构如下：

```json
{
  "src": "c1",
  "dest": "n1",
  "body": {
    "type": "...",
    "msg_id": 1
  }
}
```

字段说明：
- `src`：消息的发送者（比如客户端 `c1`）
- `dest`：消息的接收者（比如节点 `n1`）
- `body`：消息体，其中 `type` 表示消息类型，`msg_id` 是可选的消息编号

**要求：**
1. 从标准输入逐行读取（每行是一个完整的 JSON 对象）
2. 解析出 `src`、`dest` 和 `body.type` 三个字段
3. 按格式 `PARSED: src|dest|body_type` 输出到标准输出
4. 可以把调试信息输出到标准错误（stderr），不会影响评判
5. 持续读取直到标准输入关闭

## 概念说明

### 基于消息的通信

分布式系统之所以通过消息通信，是因为各节点运行在不同的机器上，内存空间彼此隔离。

打个比方：单机程序里的多个线程就像住在同一个房间里的人，可以直接看到彼此桌上的东西（共享内存）。而分布式系统中的节点就像住在不同城市的人，只能通过写信（发消息）来交流。

这种通信方式带来了几个关键挑战：
- **网络不可靠** —— 消息可能延迟、重复，甚至丢失
- **故障是局部的** —— 有些节点可能已经崩溃，但其他节点还在正常运行
- **消息必须自包含** —— 每条消息都要携带足够的信息，让接收方能独立处理

### Maelstrom 协议

Maelstrom 使用一种简单的 JSON 协议，每条消息必须包含三个字段：
- `src` —— 标识消息的发送方
- `dest` —— 标识消息的接收方
- `body` —— 消息的实际内容，其中必须包含 `type` 字段

### 为什么用 stdin/stdout？

使用标准输入输出让协议与编程语言无关。无论你用 Java、Python 还是 Go 来写节点程序，Maelstrom 都能启动你的程序并通过 stdin/stdout 与之通信。这种模式在真实系统中也很常见，叫做进程间通信（IPC）。

### 消息流转示例

```text
客户端 (c1) --> 节点 (n1)
{
  "src": "c1",
  "dest": "n1",
  "body": {"type": "echo", "msg_id": 1, "echo": "hello"}
}

节点 (n1) --> 客户端 (c1)
{
  "src": "n1",
  "dest": "c1",
  "body": {"type": "echo_ok", "msg_id": 0, "in_reply_to": 1, "echo": "hello"}
}
```

## 涉及概念

- `JSON parsing`
- `stdin/stdout`
- `message format`

## 实现提示

- 从标准输入逐行读取，每行是一个完整的 JSON 对象
- 解析 JSON 后，提取 `src`、`dest` 和 `body` 中的 `type` 字段
- 按 `PARSED: src|dest|body_type` 格式输出到标准输出
- 如果 `type` 字段不存在，可以用 `"unknown"` 作为默认值
- 调试信息输出到 stderr，不会影响评判结果

## 测试用例

### 1. 解析单条消息并提取字段

解析 JSON 消息，按 `PARSED: src|dest|body_type` 格式输出。应提取出 src=c1、dest=n1、type=echo。

输入：

```json
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":1}}
```

期望输出：

```text
PARSED: c1|n1|echo
```

## 参考资料

- [Maelstrom Protocol Specification](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md)：Maelstrom 协议的官方文档，描述了消息格式和语义
- [Python JSON Module](https://docs.python.org/3/library/json.html)：Python 标准库的 JSON 解析文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
