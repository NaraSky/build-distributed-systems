# 实现 Fault Tolerance in MapReduce

英文标题：Implement Fault Tolerance in MapReduce
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-4-fault-tolerance>

课程：30. MapReducer：批处理与流处理
任务序号：4
短标题：Fault Tolerance
难度：advanced
子主题：MapReduce Fundamentals

## 中文导读

本题要求你完成 `实现 Fault Tolerance in MapReduce`。

重点关注：`fault tolerance`、`worker failure`、`task retry`、`heartbeat`、`speculative execution`。

建议先按提示逐步实现：A worker is failed if now - last_heartbeat > timeout_ms。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Long-running MapReduce jobs will inevitably encounter worker failures. 故障 tolerance means detecting failures quickly和retrying the affected tasks on healthy workers without restarting the entire job.

Your 节点 (the master) must handle these 消息:

```JSON
// Record a 心跳 from a worker
{ "type": "心跳", "msg_id": 1, "worker_id": "w1", "timestamp": 1700000000000 }
→ { "type": "heartbeat_ok", "in_reply_to": 1 }

// Check which workers have timed out (no 心跳用于> timeout_ms)
{ "type": "check_failures", "msg_id": 2, "timeout_ms": 5000, "now": 1700000010000 }
→ { "type": "failures_detected", "in_reply_to": 2, "failed_workers": ["w2"] }

// Reassign all tasks from a failed worker to a healthy one
{ "type": "reassign", "msg_id": 3, "failed_worker": "w2", "healthy_worker": "w3",
  "tasks": [{"id": "t1", "chunk": ["hello world"]}] }
→ { "type": "reassigned", "in_reply_to": 3, "reassigned_tasks": ["t1"] }
```

A worker is considered failed when `now - last_heartbeat_timestamp > timeout_ms`. Tasks assigned to failed workers are retried — they are idempotent, so running them again on a different worker is always safe.

## 涉及概念

- `fault tolerance`
- `worker failure`
- `task retry`
- `heartbeat`
- `speculative execution`
- `idempotence`

## 实现提示

- A worker is failed if now - last_heartbeat > timeout_ms
- On 故障, find all tasks assigned to that worker和re-队列 them
- Tasks must be idempotent: re-running produces the same result
- Speculative execution: if a task is running too long, start it on a second worker
- Use task attempts 计数器; drop the result from the slower duplicate

## 测试用例

### 1. Record heartbeat

Should acknowledge 心跳 from worker.

输入：

```json
{"src":"w1","dest":"master","body":{"type":"heartbeat","msg_id":1,"worker_id":"w1","timestamp":1700000000000}}
```

期望输出：

```text
{"type": "heartbeat_ok", "in_reply_to": 1}
```

### 2. Detect timed-out worker

10s elapsed > 5s 超时, so w1 should be failed.

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

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/)：Section 3.3 covers 故障 tolerance in the original paper

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
