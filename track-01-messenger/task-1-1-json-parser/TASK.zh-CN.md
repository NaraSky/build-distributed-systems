# 实现 基础 JSON 消息 解析器

英文标题：Implement Basic JSON Message Parser
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-1-json-parser>

课程：1. 信使：消息通信基础
任务序号：1
短标题：JSON 解析器
难度：beginner
子主题：Hello, Distributed World

## 中文导读

本题要求你完成 `实现 基础 JSON 消息 解析器`。

重点关注：`JSON parsing`、`stdin/stdout`、`message format`。

建议先按提示逐步实现：Read one line at a time from 标准输入。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In 分布式系统, 节点 communicate by exchanging 消息. The Maelstrom framework uses JSON 消息 over 标准输入/标准输出用于simplicity和language-agnosticism.

Your task is to implement a basic 消息 parser that reads JSON 消息 from 标准输入. Each 消息 has the following structure:

```JSON
{
  "src": "c1",        // Source 节点 ID
  "dest": "n1",       // Destination 节点 ID
  "body": {           // 消息 payload
    "type": "...",    // 消息 type
    "msg_id": 1       // Optional 消息 ID
  }
}
```

Read 消息 from 标准输入 (one JSON object per line), parse them,和**print the parsed fields to 标准输出** in the format: `PARSED: src|dest|body_type`. Also 日志 detailed information to 标准错误用于debugging.

Your 节点 should continue reading until 标准输入 is closed.

## 概念说明

## 消息-Based Communication

分布式系统 communicate through **消息** because 节点 cannot share memory. This is a fundamental constraint that shapes how we design distributed algorithms.

### Why Messages?

In a single-machine program, threads can share memory directly. But in a distributed system:

  - **节点 are on different machines** - they have separate memory spaces

  - **Networks are unreliable** - 消息 can be delayed, duplicated, or lost

  - **Failures are partial** - some 节点 may crash while others continue

Each 消息 must be *self-contained*，包含enough information用于the recipient to process it independently.

### The Maelstrom Protocol

Maelstrom uses a simple JSON-based protocol，包含three required fields:

  - `src` - identifies who sent the 消息

  - `dest` - identifies the intended recipient

  - `body` - contains the actual payload，包含a `type` field

### Why stdin/stdout?

Using standard streams makes the protocol **language-agnostic**. Maelstrom can spawn your binary和communicate，包含it regardless of what language you wrote it in. This same pattern is used by many real systems用于inter-process communication (IPC).

### 消息 Flow Example

```text
Client (c1) -->节点(n1)
{
  "src": "c1",
  "dest": "n1", 
  "body": {"type": "echo", "msg_id": 1, "echo": "hello"}
}

Node (n1) --> Client (c1)
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

- Read one line at a time from 标准输入
- Each line is a complete JSON object
- Parse the 消息和extract src, dest,和body fields
- Print "PARSED: src|dest|body_type" to 标准输出用于validation
- Use .get("type", "unknown") to handle missing type field gracefully

## 测试用例

### 1. Parse single 消息和extract fields

Must parse JSON和output "PARSED: src|dest|body_type" format. Should extract src=c1, dest=n1, type=echo.

输入：

```json
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":1}}
```

期望输出：

```text
PARSED: c1|n1|echo
```

## 参考资料

- [Maelstrom Protocol Specification](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md)：Official protocol documentation describing 消息 format和semantics
- [Python JSON Module](https://docs.python.org/3/library/json.html)：Python standard library documentation用于JSON parsing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
