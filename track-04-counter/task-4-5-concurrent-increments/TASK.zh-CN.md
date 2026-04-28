# 处理多节点并发递增

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-5-concurrent-increments>

课程：4. 计数器：分布式状态与 CRDT
任务序号：5
短标题：并发更新
难度：高级
子主题：丢失更新问题

## 中文导读

这道题让你在高并发负载下测试 G-Counter 的正确性。多个节点会同时进行递增操作，最终的读取值必须等于所有递增量的总和。这是对你 CRDT 实现的真正考验，你需要让节点之间通过 gossip 协议同步状态。

## 题目说明

在高并发负载下测试你的 G-Counter。多个节点会同时进行递增操作，最终读取到的值必须等于所有递增操作的总和。

## 概念说明

### 最终一致性

如果 CRDT 实现正确，所有节点最终都会收敛到相同的值。G-Counter 能保证这一点，即使在网络分区和消息延迟任意的情况下也不例外。就像各地的投票站分别统计选票，最终汇总时一定能得到正确的总数。

## 涉及概念

- `concurrent operations`
- `distributed testing`
- `verification`

## 实现提示

- 定期通过 gossip 协议将你的 G-Counter 状态广播给其他节点
- 收到其他节点的状态时，将其合并到本地状态中
- 所有节点最终应该收敛到相同的值

## 测试用例

### 1. 本地递增正确累加

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":10}}
{"src":"c2","dest":"n1","body":{"type":"add","msg_id":3,"delta":20}}
{"src":"c3","dest":"n1","body":{"type":"add","msg_id":4,"delta":30}}
{"src":"c4","dest":"n1","body":{"type":"read","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c2", "body": {"type": "add_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c3", "body": {"type": "add_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "n1", "dest": "c4", "body": {"type": "read_ok", "value": 60, "in_reply_to": 5, "msg_id": 4}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
