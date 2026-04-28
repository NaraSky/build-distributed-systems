# 添加消息信封校验

英文标题：Add Message Envelope Validation
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-4-envelope-validation>

课程：1. 信使：消息通信基础
任务序号：4
短标题：信封校验
难度：入门
子主题：Hello, Distributed World

## 中文导读

这道题让你给节点加上"防御能力"：在真正处理消息之前，先检查消息的格式是否正确。如果收到了格式错误的消息，节点不能崩溃，而应该记录一条错误日志后继续运行。

在真实的分布式系统中，网络上什么样的数据都可能收到，健壮的输入校验是保证节点稳定运行的关键。

## 题目说明

生产环境的系统必须能优雅地处理格式错误的输入。你的节点应该在处理消息之前，先验证消息是否具有正确的结构。

需要校验的内容包括：

1. 消息必须是合法的 JSON
2. 消息必须包含 `src`、`dest` 和 `body` 三个字段
3. `body` 中必须包含 `type` 字段
4. 对于需要响应的请求，`body` 中应该包含 `msg_id`

如果校验失败，将错误信息输出到标准错误（stderr），但**不要崩溃**。这种防御性编程可以防止单条错误消息导致整个节点崩溃。

## 概念说明

### 防御性编程

在分布式系统中，你**不能信任网络和其他节点**。消息可能损坏、截断或格式完全错误。你的节点必须校验输入，并在遇到问题时优雅地处理。

打个比方：就像收快递时先检查包裹是否完好再签收一样，节点收到消息后也要先检查格式是否正确再处理。

### 为什么校验很重要

如果不做校验会怎样？

- **崩溃** —— 访问不存在的字段会抛出异常
- **安全漏洞** —— 格式错误的输入可能被恶意利用
- **级联故障** —— 一条错误消息就能让整个节点宕机

### 校验策略

好的校验策略是在系统的**边界处**检查输入：

```text
def validate_message(msg):
    # Check structure
    if not isinstance(msg, dict):
        return False, "Message must be an object"
    
    # Check required fields
    for field in ["src", "dest", "body"]:
        if field not in msg:
            return False, f"Missing field: {field}"
    
    # Check body structure
    if "type" not in msg["body"]:
        return False, "Body missing type field"
    
    return True, None
```

### 错误语义

Maelstrom 定义了类型为 `error` 的错误响应，包含错误码和描述信息：

```text
{
  "type": "error",
  "in_reply_to": 1,
  "code": 10,
  "text": "Node not initialized"
}
```

常见的错误码：

- `0` —— 超时
- `1` —— 节点未找到
- `10` —— 不支持的操作
- `11` —— 暂时不可用
- `12` —— 请求格式错误

## 涉及概念

- `validation`
- `error handling`
- `defensive programming`

## 实现提示

- 检查必需字段是否存在
- 优雅地处理格式错误的 JSON（不要崩溃）
- 将校验错误信息输出到 stderr

## 测试用例

### 1. 处理合法消息

收到格式正确的消息时，应正常处理并返回响应。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Maelstrom Error Codes](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md#errors)：Maelstrom 错误响应格式和错误码的官方参考

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
