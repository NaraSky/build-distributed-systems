# 用类型化模式定义消息格式

英文标题：Model Message Format with Typed Schema
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-1-typed-schema>

课程：1. 信使：消息通信基础
任务序号：11
短标题：类型化模式
难度：进阶
子主题：协议底层机制

## 中文导读

前面的题目中，我们直接操作原始的 JSON 字符串。但原始 JSON 只是一堆字符串，很容易因为拼错字段名、漏掉必填字段而发送出格式错误的消息。这道题要求你定义类型化的消息类（Message、MessageBody），通过类的字段和方法来保证消息格式的正确性。

类型化模式是构建可靠分布式系统的重要实践——在真实项目中，Protocol Buffers、Avro 等序列化框架做的就是这件事。

## 题目说明

原始 JSON 只是一串字符。如果直接手动拼 JSON，很容易出错——少写一个字段、拼错一个字段名，编译器都不会报错，只有在运行时才会发现问题。

**类型化模式（Typed Schema）**的做法是：把原始消息包装成带有明确字段定义的类，并提供验证和序列化方法。这样一来，发送格式错误的消息就变成了编译时错误，而不是运行时意外。

你的任务是：

1. 实现一个 `Message` 类，包含 `src`、`dest`、`body` 字段，以及 `to_json()` / `from_json()` 方法
2. 实现一个 `MessageBody` 类，至少包含 `type`、`msg_id`、`in_reply_to` 字段
3. 你的节点需要处理 `init`、`echo` 消息，以及一个新的 `validate` 消息类型

`validate` 消息的工作方式如下：

```json
{ "type": "validate", "msg_id": 1,
  "payload": "{\"src\":\"a\",\"dest\":\"b\",\"body\":{\"type\":\"x\"}}" }
-> { "type": "validate_ok", "in_reply_to": 1,
    "valid": true, "fields": ["src", "dest", "body.type"] }
```

`validate` 处理器会解析 `payload` 中的 JSON 字符串，并报告其中存在哪些顶层字段和嵌套字段。如果 `payload` 不是合法的 JSON，则返回 `valid: false` 和空的 `fields` 列表。

## 概念说明

### 为什么需要类型化模式

打个比方：没有类型化模式的消息就像手写信封——你可能写错收件人地址、漏写邮编，邮局（运行时）才会发现问题。有了类型化模式，就像使用预印好格式的信封——每个字段都有固定位置，漏填了一目了然。

### 序列化与反序列化

**序列化（Serialization）**是把内存中的对象转换成可以传输的格式（比如 JSON 字符串）。**反序列化（Deserialization）**是反过来，把收到的字符串还原成内存中的对象。类型化模式在反序列化时可以做验证，确保收到的数据符合预期格式。

### 现实中的应用

Google 的 Protocol Buffers、Apache 的 Avro、Facebook 的 Thrift 都是类型化消息模式的典型代表。它们在分布式系统中被广泛使用，既保证了消息格式的正确性，又支持协议的版本演进。

## 涉及概念

- `serialization`
- `deserialization`
- `schema design`
- `type safety`

## 实现提示

- 定义一个 Message 类，包含 `src`、`dest` 和 `body` 字段
- MessageBody 至少包含 `type`、`msg_id` 和 `in_reply_to` 字段
- 实现 `to_json()` 和 `from_json()` 方法来处理序列化
- 在反序列化时验证字段类型
- 对缺失的可选字段使用合理的默认值

## 测试用例

### 1. 使用类型化模式处理初始化和回声

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"typed"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "typed", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 验证一个格式正确的消息载荷

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"validate","msg_id":2,"payload":"{\"src\":\"a\",\"dest\":\"b\",\"body\":{\"type\":\"x\"}}"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "validate_ok", "valid": true, "fields": ["src", "dest", "body.type"], "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Protocol Buffers Overview](https://protobuf.dev/overview/)：Google 如何为分布式系统定义类型化消息模式

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
