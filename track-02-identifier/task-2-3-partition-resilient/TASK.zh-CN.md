# 实现 ID Generation During Network Partition

英文标题：Implement ID Generation During Network Partition
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-partition-resilient>

课程：2. 标识符：分布式唯一 ID
任务序号：3
短标题：Partition Resilient
难度：intermediate
子主题：Why 唯一 IDs Are Hard

## 中文导读

本题要求你完成 `实现 ID Generation During Network Partition`。

重点关注：`network partitions`、`availability`、`CAP theorem`。

建议先按提示逐步实现：Your ID generation should work without 网络 access。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

分布式系统 must handle **网络 partitions** - times when 节点 cannot communicate，包含each other. Your ID generator must continue working even when completely isolated from other 节点.

Test your implementation by verifying it works when:

1. The 节点 cannot reach any other 节点
2. The 网络 has high latency
3. 消息 are being dropped

A good ID generation scheme is **fully local**和does not require coordination，包含other 节点.

## 概念说明

## CAP Theorem和Availability

The CAP theorem states that during a 网络 partition, you can have either **Consistency** or **Availability**, but not both.

ID generation should prioritize **availability**: even an isolated 节点 should generate valid IDs.

### Local-First Design

By embedding the `node_id` in our IDs, we achieve partition tolerance. Each 节点 can independently generate IDs that are guaranteed unique across the 集群, *without coordination*.

### The Trade-off

  
    Approach
    Consistency
    Availability
  
  
    Central ID server
    Strong (sequential IDs)
    Fails during partition
  
  
    Node-embedded IDs
    Weak (no ordering)
    Always available
  

### 时钟 Drift处理

What if the 时钟 goes *backwards*? This can happen，包含NTP adjustments. A robust implementation should:

  - Detect backward 时钟 movement

  - Wait until timestamp advances, OR

  - Continue使用the previous timestamp，包含incrementing sequence

## 涉及概念

- `network partitions`
- `availability`
- `CAP theorem`

## 实现提示

- Your ID generation should work without 网络 access
- Do not depend on other 节点 or external services
- Consider what happens if clocks drift
- Generated IDs must be globally unique - use timestamp + node_id + sequence to guarantee no collisions even under partition

## 测试用例

### 1. Generate 基础 ID

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
```

## 参考资料

- [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)：Understanding the trade-offs in 分布式系统

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
