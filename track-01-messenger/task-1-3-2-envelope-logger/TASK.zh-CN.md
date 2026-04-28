# 添加带时间戳的消息信封日志器

英文标题：Add Message Envelope Logger with Timestamps
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-2-envelope-logger>

课程：1. 信使：消息通信基础
任务序号：12
短标题：信封日志器
难度：进阶
子主题：协议底层机制

## 中文导读

在生产环境中，当分布式系统出了问题，你最需要的信息就是："这个节点在什么时间、发了什么消息、收了什么消息？"这道题要求你给节点加上消息日志功能，记录每条收发消息的时间戳、方向、来源、目标和类型。

消息追踪是分布式系统可观测性（Observability）的基础，也是排查问题时最重要的工具之一。

## 题目说明

在生产级别的分布式系统中，**消息追踪（Message Tracing）**对调试至关重要。当系统出现问题时，你需要能回答这个问题："这个节点发了和收了哪些消息？分别在什么时候？"

你的任务是给节点添加一个消息信封日志器：

1. 每收到一条消息，记录日志：时间戳、方向（RECV）、发送者、接收者、消息类型
2. 每发出一条消息，记录日志：时间戳、方向（SENT）、发送者、接收者、消息类型
3. 日志存储在内存缓冲区中，保留最近 100 条记录
4. 实现 `get_log` 消息类型，用于查询日志条目

```json
Request:  {"type": "get_log", "msg_id": 1, "count": 5}
Response: {"type": "get_log_ok", "in_reply_to": 1, "entries": [
    {"ts": "2024-01-01T00:00:00", "dir": "RECV", "src": "c0", "dest": "n1", "msg_type": "init"},
    {"ts": "2024-01-01T00:00:00", "dir": "SENT", "src": "n1", "dest": "c0", "msg_type": "init_ok"}
]}
```

`count` 字段指定返回最近多少条日志。如果实际条目不够，就返回所有已有的。

## 概念说明

### 什么是消息信封

"信封（Envelope）"这个比喻很形象：就像你寄信时信封上写着寄件人、收件人和邮戳，消息信封日志记录的也是这些"外层"信息——谁发的、发给谁、什么时候发的、什么类型的消息。你不需要记录消息体的全部内容，只记录信封信息就够了。

### 为什么要追踪消息

在单机程序中，你可以用调试器一步步跟踪代码执行。但在分布式系统中，多个节点并行运行，没有全局的执行顺序。消息日志让你事后可以"回放"每个节点的通信过程，像侦探一样还原事件经过。

### 内存缓冲区的设计

保留最近 100 条记录是一个典型的有界缓冲区设计。在实际系统中，日志通常会写到磁盘或发送到集中式日志系统（如 ELK、Loki），但在本题中使用内存缓冲区就够了。

## 涉及概念

- `logging`
- `observability`
- `message tracing`
- `timestamps`

## 实现提示

- 每条消息记为一行日志，带上时间戳前缀
- 包含方向（SENT 或 RECV）、发送者、接收者和消息类型
- 时间戳使用 ISO 8601 格式
- 日志输出到标准错误（stderr），避免干扰标准输出的消息传递
- 实现 `get_log` 消息类型，返回最近的日志条目

## 测试用例

### 1. 初始化和回声功能正常输出

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"log-test"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "log-test", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 初始化后获取日志条目

第二行输出是 `get_log_ok`，其中的 `entries` 包含 RECV init、SENT init_ok 和 RECV get_log。由于时间戳的具体值会变化，测试只检查结构是否正确。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"get_log","msg_id":2,"count":10}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Distributed Tracing](https://opentelemetry.io/docs/concepts/observability-primer/)：OpenTelemetry 关于分布式系统可观测性的入门指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
