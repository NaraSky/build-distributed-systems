# Validate Uniqueness Across Distributed Nodes

英文标题：Validate Uniqueness Across Distributed Nodes
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-uniqueness-validation>

课程：2. 标识符：分布式唯一 ID
任务序号：4
短标题：Uniqueness 校验
难度：intermediate
子主题：Why 唯一 IDs Are Hard

## 中文导读

本题要求你完成 `Validate Uniqueness Across Distributed Nodes`。

重点关注：`testing`、`verification`、`global uniqueness`。

建议先按提示逐步实现：Maelstrom will verify uniqueness automatically。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Run your ID generator through Maelstrom verification to prove uniqueness. Maelstrom collects all generated IDs across all 节点和checks用于duplicates.

Your implementation must pass with:

- Multiple 节点 generating concurrently
- High throughput (thousands of IDs per second)
- 网络 partitions separating 节点

Think about **why** your scheme guarantees uniqueness. What assumptions does it make? What could cause collisions?

## 概念说明

## Proving Uniqueness

A strong ID scheme should have a **provable uniqueness guarantee**.

### The Proof Structure

If IDs combine:

  - `node_id` - unique per 节点

  - `timestamp` - monotonic

  - `sequence` - unique per timestamp

Then uniqueness is guaranteed as long as:

  - 节点 IDs are unique

  - Clocks do not go backwards more than a tolerable amount

  - Sequence does not overflow

### Failure模式s

  
    Failure
    Cause
    Mitigation
  
  
    Clock sync issue
    NTP adjustment
    Wait or use previous timestamp
  
  
   节点ID reuse
   节点restart，包含same ID
    Persist counter or use epoch
  
  
    Sequence overflow
    >4096 IDs/ms
    Wait用于next millisecond

## 涉及概念

- `testing`
- `verification`
- `global uniqueness`

## 实现提示

- Maelstrom will verify uniqueness automatically
- Consider mathematical proof of your ID uniqueness
- Document your uniqueness guarantees

## 测试用例

### 1. Generate two IDs，包含正确的 format

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
{"src":"c2","dest":"n1","body":{"type":"generate","msg_id":3}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
{"src":"n1","dest":"c2","body":{"type":"generate_ok","in_reply_to":3,"msg_id":2,"id":"n1-1"}}
```

## 参考资料

- [Maelstrom Unique IDs Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-unique-ids)：Specification用于the unique-ids workload

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
