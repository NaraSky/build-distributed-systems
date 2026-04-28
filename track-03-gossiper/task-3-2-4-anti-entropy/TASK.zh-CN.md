# 实现基于摘要比对的反熵同步

英文标题：Implement Anti-Entropy with Digest Comparison
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-4-anti-entropy>

课程：3. 传播者：Gossip 信息传播
任务序号：9
短标题：反熵同步
难度：高级
子主题：Gossip 协议

## 中文导读

这道题解决的是一个实际问题：当节点之间的数据大部分已经同步时，每次都传输完整状态太浪费带宽了。反熵（Anti-Entropy）通过先交换紧凑的摘要信息来判断双方是否一致，只在不一致时才传输完整数据。这就像两个人对账——先比一下总数，总数一样就不用逐条核对了。

## 题目说明

当节点之间的数据大部分已经同步时，传输完整状态会浪费大量带宽。**反熵**（Anti-Entropy）对此进行了优化：先交换紧凑的摘要信息，只有在摘要不一致时才传输完整状态。

实现基于摘要的反熵同步：

1. `digest` 处理器：返回当前消息集合的哈希摘要
2. `digest_sync` 处理器：比较摘要，仅在不一致时传输数据
3. 跟踪带宽节省情况

```json
Request:  {"type": "digest", "msg_id": 1}
Response: {"type": "digest_ok", "in_reply_to": 1, "digest": "abc123", "count": 5}
```

```json
Request:  {"type": "digest_sync", "msg_id": 2, "remote_digest": "abc123", "remote_messages": null}
Response: {"type": "digest_sync_ok", "in_reply_to": 2, "match": true, "transferred": 0}
```

如果摘要不一致，远端会发送它的消息列表：
```json
Request:  {"type": "digest_sync", "msg_id": 3, "remote_digest": "xyz789", "remote_messages": [1,2,3]}
Response: {"type": "digest_sync_ok", "in_reply_to": 3, "match": false, "transferred": 2, "local_messages": [1,2,3,4,5]}
```

## 涉及概念

- `anti-entropy`
- `digest`
- `set reconciliation`
- `bandwidth optimization`

## 实现提示

- 摘要是对当前状态的一个紧凑概括（例如，对所有消息 ID 排序后取哈希值）
- 先比较摘要；只有在摘要不同时才传输完整状态
- 当节点之间大部分数据一致时，这种方式能显著节省带宽
- 可以使用排序后的消息 ID 列表的简单哈希作为摘要
- 记录使用摘要比对相对于全量同步所节省的字节数

## 测试用例

### 1. 空集合的摘要

验证说明：`digest_ok` 的响应中，`count` 应为 0，`digest` 应是一个非空字符串。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"digest","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 摘要匹配时的同步

验证说明：`digest_ok` 的响应中，`count` 应为 1。返回的摘要值可用于后续的 `digest_sync` 操作。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"digest","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Merkle Trees for Anti-Entropy](https://en.wikipedia.org/wiki/Merkle_tree)：默克尔树如何实现高效的集合协调

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
