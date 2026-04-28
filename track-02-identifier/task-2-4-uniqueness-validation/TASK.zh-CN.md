# 验证分布式节点间的 ID 唯一性

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-uniqueness-validation>

课程：2. 标识符：分布式唯一 ID
任务序号：4
短标题：唯一性验证
难度：进阶
子主题：为什么唯一 ID 这么难

## 中文导读

这道题让你用 Maelstrom 测试框架来验证 ID 生成器的正确性。Maelstrom 会收集所有节点生成的全部 ID，并检查是否有重复。这是从"觉得正确"到"证明正确"的关键一步。

## 题目说明

将你的 ID 生成器放到 Maelstrom 验证框架中运行，以证明其唯一性。Maelstrom 会收集所有节点生成的全部 ID，然后检查是否存在重复。

你的实现必须在以下条件下通过验证：

- 多个节点同时并发生成 ID
- 高吞吐量（每秒数千个 ID）
- 网络分区导致节点被隔离

请思考：你的方案**为什么**能保证唯一性？它依赖了哪些假设？什么情况下可能产生冲突？

## 概念说明

### 证明唯一性

一个好的 ID 方案应该有**可证明的唯一性保证**。

### 证明的结构

如果 ID 由以下三部分组成：

  - `node_id` - 每个节点唯一

  - `timestamp` - 单调递增

  - `sequence` - 每个时间戳内唯一

那么只要满足以下条件，唯一性就能得到保证：

  - 节点 ID 不重复

  - 时钟回退不超过可容忍的范围

  - 序列号不会溢出

### 失败场景分析

  
    失败类型
    原因
    应对策略
  
  
    时钟同步问题
    NTP 调整
    等待或沿用上一个时间戳
  
  
    节点 ID 重用
    节点用相同 ID 重启
    持久化计数器或使用纪元
  
  
    序列号溢出
    每毫秒超过 4096 个 ID
    等待下一个毫秒

## 涉及概念

- `testing`
- `verification`
- `global uniqueness`

## 实现提示

- Maelstrom 会自动验证唯一性
- 思考一下你的 ID 唯一性的数学证明
- 记录你的唯一性保证条件

## 测试用例

### 1. 生成两个格式正确的 ID

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

- [Maelstrom Unique IDs Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-unique-ids)：Maelstrom 唯一 ID 工作负载的规范说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
