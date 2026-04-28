# 实现回调清理器：处理泄漏的 RPC

英文标题：Implement Callback Reaper for Leaked RPCs
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-4-callback-reaper>

课程：1. 信使：消息通信基础
任务序号：9
短标题：回调清理器
难度：进阶
子主题：RPC 与请求-响应模型

## 中文导读

当节点发出一个异步 RPC 请求后，如果对方崩溃了或者网络把消息弄丢了，注册的回调函数就会永远留在内存里，造成资源泄漏。这道题要求你实现一个"回调清理器（Callback Reaper）"，定期扫描并清理超时的回调。

这是分布式系统中非常实际的问题——任何需要等待远端响应的系统，都必须考虑"等不到回复怎么办"。学会处理资源泄漏，是写出健壮分布式程序的基本功。

## 题目说明

当一个节点（Node）发送异步 RPC 请求时，会注册一个回调函数（Callback），等对方回复后再执行。但如果对方节点崩溃了，或者网络把消息丢了，这个回调就永远不会被触发，却一直占着内存。这就是**资源泄漏（Resource Leak）**，随着时间推移，可能耗尽所有可用内存。

你的任务是实现一个**回调清理器**，它需要：

1. 在注册每个回调时记录时间戳
2. 定期扫描所有回调，找出超过阈值（默认 2 秒）的回调
3. 删除过期的回调，并以超时错误调用它们（通知调用方"超时了"）
4. 报告清理了多少个回调

需要实现 `pending_count` 消息类型，用于查询当前有多少个等待中的回调：

```json
Request:  {"type": "pending_count", "msg_id": 1}
Response: {"type": "pending_count_ok", "in_reply_to": 1, "count": 5}
```

还需要实现 `send_fire_forget` 消息类型，用于发送一个不期望回复的 RPC（模拟会泄漏的回调）：

```json
Request:  {"type": "send_fire_forget", "msg_id": 1, "target": "n2", "payload": {"type": "echo", "echo": "lost"}}
Response: {"type": "send_fire_forget_ok", "in_reply_to": 1, "pending": 1}
```

## 概念说明

### 资源泄漏

打个比方：你给朋友寄了一封信，然后一直站在邮箱旁边等回信。如果朋友搬家了（节点崩溃）或者信在路上丢了（网络丢包），你就会一直等下去，永远占着邮箱旁边的位置。在程序里，这个"占着的位置"就是回调函数占用的内存。

### 回调清理器的工作原理

回调清理器就像一个定时巡逻的保安：每隔一段时间检查一次，把等待时间超过阈值的回调标记为"超时"，然后清理掉。被清理的回调会收到一个超时错误通知，这样上层代码就知道"对方没有回复，需要采取其他措施"。

### 为什么不能直接丢弃

直接删除超时回调而不通知调用方是不行的，因为调用方可能还在等结果。正确的做法是：清理回调的同时，用一个超时错误来调用它，让调用方知道发生了什么。

## 涉及概念

- `resource cleanup`
- `memory leaks`
- `periodic tasks`
- `garbage collection`

## 实现提示

- 在注册每个回调时，同时记录当前时间戳
- 定期扫描回调字典，找出已过期的条目
- 可以使用 `System.currentTimeMillis()` 获取当前时间（毫秒）
- 清理器的扫描间隔设为 500 毫秒是一个合理的起点
- 清理回调时，用一个错误值或 null 来调用它，以表示超时

## 测试用例

### 1. 待处理回调数初始为零

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pending_count","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "pending_count_ok", "count": 0, "in_reply_to": 2, "msg_id": 1}}
```

### 2. 发射后不管的消息会增加待处理回调数

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"send_fire_forget","msg_id":2,"target":"n2","payload":{"type":"echo","echo":"lost"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "echo", "echo": "lost", "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "send_fire_forget_ok", "pending": 1, "in_reply_to": 2, "msg_id": 2}}
```

## 参考资料

- [Resource Leaks in Distributed Systems](https://sre.google/sre-book/handling-overload/)：Google SRE 手册中关于资源限制和过载管理的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
