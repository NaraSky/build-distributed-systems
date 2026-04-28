# 处理树节点故障并实现直接投递回退

英文标题：Handle Tree Node Failure with Direct Fallback
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-2-tree-failure>

课程：3. 传播者：Gossip 信息传播
任务序号：12
短标题：树节点故障
难度：高级
子主题：Topology-Aware Gossip

## 中文导读

这道题让你解决树广播的"脆弱性"问题。树广播虽然高效，但一旦某个节点崩溃，它下方的整棵子树都会失联。你需要加入故障检测机制：当发现子节点没有按时回复确认时，自动切换到直接投递模式，把消息直接发给可能受影响的节点。这是分布式系统中容错设计的典型练习。

## 题目说明

树广播效率高，但也很脆弱：如果某个节点崩溃了，它的所有后代节点都会失去连接。你的任务是为树广播添加**故障检测**机制，并在检测到故障时回退到直接投递方式。

具体来说，当你向邻居转发消息时，需要期待对方在超时时间内回复一个 `broadcast_ack`。如果超时未收到确认，就回退到直接投递模式，把消息直接发送给所有可能在故障子树中的节点。

需要实现以下功能：
1. 带确认追踪的 `broadcast` 广播
2. 处理 `broadcast_ack` 确认消息
3. `check_acks` 处理器，用于模拟超时检查并触发回退投递
4. `failure_stats` 用于报告故障统计信息

```json
请求:  {"type": "check_acks", "msg_id": 1}
响应: {"type": "check_acks_ok", "in_reply_to": 1, "pending": 2, "timed_out": 1, "direct_sent": 3}
```

```json
请求:  {"type": "failure_stats", "msg_id": 2}
响应: {"type": "failure_stats_ok", "in_reply_to": 2, "total_failures": 1, "direct_deliveries": 3}
```

## 涉及概念

- `fault tolerance`
- `tree failure`
- `ack timeout`
- `direct delivery`

## 实现提示

- 当一个子节点崩溃时，它下方的整棵子树都会"失联"
- 为每个子节点的确认设置超时追踪
- 如果 500 毫秒内未收到确认，就直接把消息发给已知的下游节点
- 维护一个包含所有节点的列表，用于直接投递的回退方案
- 将投递失败的信息输出到标准错误流，便于调试

## 测试用例

### 1. 没有邻居时的广播

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [42], "in_reply_to": 4, "msg_id": 3}}
```

### 2. 故障统计初始值为零

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"failure_stats","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "failure_stats_ok", "total_failures": 0, "direct_deliveries": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Fault-Tolerant Broadcast](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/2003-reliable-scalable.pdf)：康奈尔大学关于在不可靠网络中实现可靠广播的研究论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
