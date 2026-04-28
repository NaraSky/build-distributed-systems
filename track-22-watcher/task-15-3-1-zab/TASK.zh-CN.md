# 实现 ZAB 原子广播协议

英文标题：Implement ZAB Atomic Broadcast Protocol
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-1-zab>

课程：22. 观察者
任务序号：11
短标题：ZAB Broadcast
难度：高级
子主题：一致性与 ZAB 协议

## 中文导读

这道题要求你实现 ZAB 协议，它是 ZooKeeper 保证所有服务器数据一致的核心机制。你可以把它理解为一个"广播确认"流程：领导者收到写请求后，先把更新方案发给所有跟随者征求意见，等到超过半数的跟随者确认收到后，再正式通知大家执行。这样一来，所有服务器看到的更新顺序就完全一致了。理解这个协议是掌握 ZooKeeper 一致性保证的关键。

## 题目说明

ZAB（ZooKeeper Atomic Broadcast，ZooKeeper 原子广播）是让所有 ZooKeeper 服务器保持同步的共识协议。它的核心保证是：所有服务器以完全相同的顺序看到所有更新。

整个协议分为两个阶段，具体流程如下：

1. **提议阶段**：领导者为每个写操作分配一个单调递增的事务编号（zxid），然后将提案广播给所有跟随者。
2. **确认阶段**：每个跟随者收到提案后，将其写入本地的预写日志（WAL），然后向领导者发送确认回执。
3. **提交阶段**：当领导者收到超过半数服务器的确认（即达到法定人数）后，广播提交指令。
4. **应用阶段**：所有服务器（包括领导者和跟随者）将已提交的更新应用到内存中的 ZNode 树。

为什么这能保证顺序一致？因为事务编号是单调递增的，而且所有提案都严格按编号顺序执行，所以每台服务器上的更新序列完全相同。

协议示例：

```json
Request:  {"type": "zab_propose", "msg_id": 1, "operation": "SetData", "path": "/config", "data": "v2", "zxid": "0x100000001"}
Response: {"type": "zab_propose_ok", "in_reply_to": 1, "acks_received": 2, "quorum_size": 2, "committed": true}
```

## 涉及概念

- `ZAB`
- `atomic broadcast`
- `2-phase commit`
- `proposal`
- `quorum acknowledgement`

## 实现提示

- 领导者收到写请求后，创建一个带有唯一事务编号的提案
- 领导者将提案广播给所有跟随者
- 跟随者将提案写入本地预写日志后，向领导者发送确认
- 领导者收到超过半数的确认后，广播提交指令
- 所有服务器将已提交的提案应用到内存中的节点树

## 测试用例

### 1. 获得多数确认的提案被成功提交

验证说明：当确认数达到法定人数时，提交标志应为真。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":2,"operation":"SetData","path":"/cfg","data":"v1","zxid":"0x100000001"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 连续的事务编号保持有序

验证说明：两个提案应当严格按照事务编号的先后顺序被提交。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":2,"operation":"SetData","path":"/a","data":"1","zxid":"0x100000001"}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":3,"operation":"SetData","path":"/b","data":"2","zxid":"0x100000002"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZAB Protocol](https://zookeeper.apache.org/doc/current/zookeeperInternals.html#sc_atomicBroadcast)：ZooKeeper 官方文档中关于原子广播协议的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
