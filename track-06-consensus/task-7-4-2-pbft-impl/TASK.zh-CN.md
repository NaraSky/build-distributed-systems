# 实现简化版 PBFT（4 节点）

英文标题：Implement Simplified PBFT with 4 Nodes
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-2-pbft-impl>

课程：6. 共识
任务序号：17
短标题：PBFT Implementation
难度：高级
子主题：Byzantine Fault Tolerance

## 中文导读

本题要求你实现一个简化版的 PBFT（Practical Byzantine Fault Tolerance，实用拜占庭容错）协议，使用 4 个节点来容忍 1 个拜占庭故障节点。PBFT 是第一个能在实际系统中高效运行的拜占庭容错算法，通过三阶段协议保证即使有恶意节点存在，诚实节点仍能达成一致。这道题将帮助你从代码层面理解拜占庭容错的工作机制。

## 题目说明

实现一个简化版的 PBFT 协议，包含 4 个节点（可容忍 `f=1` 个拜占庭故障节点）。

PBFT 采用三阶段协议：
1. **预准备阶段（Pre-prepare）**：主节点为请求分配一个序列号，并向所有副本广播 `(pre-prepare, v, n, d)` 消息
2. **准备阶段（Prepare）**：每个副本向所有其他副本广播 `(prepare, v, n, d, i)` 消息。收集到 `2f` 个匹配的准备消息后，形成"准备证书"
3. **提交阶段（Commit）**：每个副本向所有其他副本广播 `(commit, v, n, d, i)` 消息。收集到 `2f+1` 个匹配的提交消息后，形成"提交证书"，请求可以被执行

```json
Request:  {"type": "pbft_request", "msg_id": 1, "operation": "set x=42", "client": "c1"}
Response: {"type": "pbft_request_ok", "in_reply_to": 1, "sequence_number": 1, "view": 0, "phase": "pre-prepare"}

Request:  {"type": "pbft_status", "msg_id": 2, "sequence_number": 1}
Response: {"type": "pbft_status_ok", "in_reply_to": 2, "phase": "committed", "prepares_received": 3, "commits_received": 4, "executed": true}
```

## 概念说明

**为什么需要三个阶段？** 两阶段不够安全——在有拜占庭节点的情况下，两阶段协议可能让不同的诚实节点得出不同的结论。第三个阶段（提交）的作用是确保所有诚实节点都知道"大家已经在准备阶段达成了一致"，从而安全地执行请求。

**`2f+1` 的含义**：在 4 个节点容忍 1 个拜占庭故障的场景下，`2f+1 = 3`。需要 3 个节点的确认才能提交，这保证了即使恶意节点参与了投票，也有至少 2 个诚实节点是真正同意的。

## 涉及概念

- `PBFT`
- `pre-prepare`
- `prepare`
- `commit`
- `three-phase protocol`

## 实现提示

- PBFT 使用三个阶段：预准备、准备、提交
- 预准备阶段：主节点将客户端请求广播给所有副本
- 准备阶段：每个副本向所有其他副本广播准备消息，等待收集到 `2f` 个匹配的准备消息
- 提交阶段：每个副本广播提交消息，等待收集到 `2f+1` 个匹配的提交消息
- 在 `f=1` 的拜占庭故障场景下，需要 `N=4` 个节点（`3f+1=4`）

## 测试用例

### 1. 请求触发预准备阶段

验证说明：响应中应显示 `sequence_number` 为 `1`、`view` 为 `0`、`phase` 为 `"pre-prepare"`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"pbft_request","msg_id":2,"operation":"set x=42","client":"c1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 所有阶段完成后显示已执行

验证说明：如果所有阶段都完成了，状态查询应显示 `phase` 为 `"committed"` 或 `"executed"`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"pbft_request","msg_id":2,"operation":"set x=1","client":"c1"}}
{"src":"c1","dest":"n1","body":{"type":"pbft_status","msg_id":3,"sequence_number":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Practical Byzantine Fault Tolerance - Castro & Liskov](https://pmg.csail.mit.edu/papers/osdi99.pdf)：PBFT 的原始论文，发表于 OSDI 1999

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
