# 实现 同步 RPC，包含超时

英文标题：Implement Synchronous RPC，包含Timeout
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-1-sync-rpc>

课程：1. 信使：消息通信基础
任务序号：6
短标题：Sync RPC
难度：intermediate
子主题：RPC和the Request-Response模式l

## 中文导读

本题要求你完成 `实现 同步 RPC，包含超时`。

重点关注：`RPC`、`synchronous communication`、`timeout`、`blocking calls`。

建议先按提示逐步实现：Use a dictionary to store pending requests keyed by msg_id。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In a distributed system, 节点 often need to call remote procedures on other 节点和wait用于the result. This is called **synchronous RPC** (Remote Procedure Call).

Your task is to extend your Maelstrom 节点，包含a `sync_rpc` method that:

1. Sends a 消息 to another 节点
2. Blocks until a 响应 is received (matched by `in_reply_to`)
3. Returns the 响应 body
4. Times out after a configurable duration (default: 1 second)

The 节点 should still handle `init`和`echo` 消息. Additionally, implement a `代理` 消息 type: when your 节点 receives a `代理` 请求, it forwards the inner 消息 to the target 节点使用`sync_rpc`, waits用于the reply,和returns it to the original caller.

```
请求:  {"type": "代理", "msg_id": 1, "target": "n2", "inner": {"type": "echo", "echo": "hello"}}
响应: {"type": "proxy_ok", "in_reply_to": 1, "result": {"type": "echo_ok", "echo": "hello", ...}}
```

For this task, simulate the remote 节点's 响应 inline (since Maelstrom test harness sends single-节点 input). Your `sync_rpc` should store callbacks和resolve them when matching replies arrive.

## 涉及概念

- `RPC`
- `synchronous communication`
- `timeout`
- `blocking calls`

## 实现提示

- Use a dictionary to store pending requests keyed by msg_id
- Block the caller使用threading.Event or a simple polling loop
- Set a 超时 so the caller does not block forever
- When a 响应 arrives, match it via in_reply_to和unblock the caller
- Return None or raise an exception if the 超时 expires

## 测试用例

### 1. 初始化和回声 still work

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"hello"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "hello", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 代理 sends RPC to target

The 节点 should forward the inner 消息 to n2 via sync_rpc. The RPC will 超时 since n2 is not present, but the outgoing 消息 to n2 must be emitted.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"proxy","msg_id":2,"target":"n2","inner":{"type":"echo","echo":"test"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "echo", "echo": "test", "msg_id": 1}}
```

## 参考资料

- [Remote Procedure Calls in Distributed Systems](https://www.cs.cornell.edu/courses/cs5414/2017fa/lectures/lec-rpc.pdf)：Cornell lecture on RPC semantics和故障 modes

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
