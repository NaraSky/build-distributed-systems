# 添加 消息 信封 校验

英文标题：Add Message Envelope Validation
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-4-envelope-validation>

课程：1. 信使：消息通信基础
任务序号：4
短标题：信封 校验
难度：beginner
子主题：Hello, Distributed World

## 中文导读

本题要求你完成 `添加 消息 信封 校验`。

重点关注：`validation`、`error handling`、`defensive programming`。

建议先按提示逐步实现：Check that required fields are present。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Production systems must handle malformed input gracefully. Your 节点 should validate that incoming 消息 have the required structure before processing.

Required validations:

1. 消息 must be valid JSON
2. 消息 must have `src`, `dest`,和`body` fields
3. Body must have a `type` field
4. For requests expecting responses, body should have a `msg_id`

If validation fails, 日志 an error to 标准错误 but do not crash. This defensive programming prevents a single bad 消息 from taking down your 节点.

## 概念说明

## Defensive Programming

In 分布式系统, you **cannot trust the 网络 or other 节点**. 消息 may be corrupted, truncated, or malformed. Your 节点 must validate inputs和fail gracefully.

### Why 校验 Matters

Consider what happens without validation:

  - **Crashes** - accessing missing fields throws exceptions

  - **Security vulnerabilities** - malformed input could be exploited

  - **Cascading failures** - one bad 消息 takes down the 节点

### 校验 Strategy

A good validation strategy checks inputs at the **boundary** of your system:

```text
def validate_message(msg):
    # Check structure
    if not isinstance(msg, dict):
        return False, "Message must be an object"
    
    # Check required fields
   用于field in ["src", "dest", "body"]:
        if field not in msg:
            return False, f"Missing field: {field}"
    
    # Check body structure
    if "type" not in msg["body"]:
        return False, "Body missing type field"
    
    return True, None
```

### Error Semantics

Maelstrom defines error responses，包含type `error`和error codes:

```text
{
  "type": "error",
  "in_reply_to": 1,
  "code": 10,
  "text": "Node not initialized"
}
```

Common error codes:

  - `0` - 超时

  - `1` - 节点 not found

  - `10` - not supported

  - `11` - temporarily unavailable

  - `12` - malformed 请求

## 涉及概念

- `validation`
- `error handling`
- `defensive programming`

## 实现提示

- Check that required fields are present
-处理malformed JSON gracefully
- 日志 validation errors to 标准错误

## 测试用例

### 1.处理valid 消息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Maelstrom Error Codes](https://github.com/jepsen-io/maelstrom/blob/main/doc/protocol.md#errors)：Reference用于error 响应 format和codes

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
