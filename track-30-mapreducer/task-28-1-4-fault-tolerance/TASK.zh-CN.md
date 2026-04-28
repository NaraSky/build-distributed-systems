# 实现 MapReduce 的容错机制

英文标题：Implement Fault Tolerance in MapReduce
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-4-fault-tolerance>

课程：30. MapReducer：批处理与流处理
任务序号：4
短标题：容错机制
难度：高级
子主题：MapReduce Fundamentals

## 中文导读

本题要求你为 MapReduce 实现容错机制。大规模分布式计算任务往往要跑很长时间，在这期间工作节点出故障是家常便饭。容错的核心思路是：通过心跳检测快速发现故障节点，然后把它的任务重新分配给健康节点来执行，而不用把整个任务从头来过。

## 题目说明

长时间运行的 MapReduce 任务不可避免地会遇到工作节点（Worker）故障。容错机制意味着快速检测故障，并在健康的工作节点上重试受影响的任务，而无需重启整个计算流程。

你的节点（主节点）必须处理以下消息：

```json
// 记录来自工作节点的心跳
{ "type": "heartbeat", "msg_id": 1, "worker_id": "w1", "timestamp": 1700000000000 }
-> { "type": "heartbeat_ok", "in_reply_to": 1 }

// 检查哪些工作节点已超时（超过 timeout_ms 未收到心跳）
{ "type": "check_failures", "msg_id": 2, "timeout_ms": 5000, "now": 1700000010000 }
-> { "type": "failures_detected", "in_reply_to": 2, "failed_workers": ["w2"] }

// 将故障工作节点的所有任务重新分配给健康节点
{ "type": "reassign", "msg_id": 3, "failed_worker": "w2", "healthy_worker": "w3",
  "tasks": [{"id": "t1", "chunk": ["hello world"]}] }
-> { "type": "reassigned", "in_reply_to": 3, "reassigned_tasks": ["t1"] }
```

当 `now - last_heartbeat_timestamp > timeout_ms` 时，认为该工作节点已故障。分配给故障节点的任务会被重试执行。由于这些任务是幂等的（执行多次结果一样），在不同的工作节点上重新执行总是安全的。

## 概念说明

心跳机制就像课堂上的点名：主节点定期检查每个工作节点是否还在"签到"。如果某个节点太久没有签到（超过了超时时间），就认为它已经"掉线"了。此时主节点会把这个节点未完成的工作交给其他在线的节点来做。由于 MapReduce 的任务天生是幂等的（同样的输入总会得到同样的输出），重复执行不会产生错误的结果，所以重新分配是完全安全的。

## 涉及概念

- `fault tolerance`
- `worker failure`
- `task retry`
- `heartbeat`
- `speculative execution`
- `idempotence`

## 实现提示

- 当 now - last_heartbeat > timeout_ms 时，认为工作节点已故障
- 故障发生时，找到分配给该工作节点的所有任务并重新排队
- 任务必须是幂等的：重复执行会产生相同的结果
- 推测执行：如果某个任务运行时间过长，可以在另一个工作节点上同时启动它的副本
- 使用任务尝试计数器；丢弃较慢的重复执行的结果

## 测试用例

### 1. 记录心跳

应确认收到来自工作节点的心跳。

输入：

```json
{"src":"w1","dest":"master","body":{"type":"heartbeat","msg_id":1,"worker_id":"w1","timestamp":1700000000000}}
```

期望输出：

```text
{"type": "heartbeat_ok", "in_reply_to": 1}
```

### 2. 检测超时的工作节点

经过 10 秒但超时阈值只有 5 秒，w1 应被判定为故障。

输入：

```json
{"src":"w1","dest":"master","body":{"type":"heartbeat","msg_id":1,"worker_id":"w1","timestamp":1700000000000}}
{"src":"monitor","dest":"master","body":{"type":"check_failures","msg_id":2,"timeout_ms":5000,"now":1700000010000}}
```

期望输出：

```text
{"type": "heartbeat_ok", "in_reply_to": 1}
{"type": "failures_detected", "in_reply_to": 2, "failed_workers": ["w1"]}
```

## 参考资料

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/)：原始论文的 3.3 节详细介绍了容错机制

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
