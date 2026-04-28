# 通过实际案例理解拜占庭故障

英文标题：Understand Byzantine Faults with Real-World Examples
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-1-byzantine-faults>

课程：6. 共识
任务序号：16
短标题：Byzantine Faults
难度：进阶
子主题：Byzantine Fault Tolerance

## 中文导读

本题带你理解什么是拜占庭故障（Byzantine Fault）。与普通的崩溃故障不同，拜占庭故障指的是节点可能"说谎"——它可以向不同的伙伴发送不同的消息，甚至故意捣乱。你需要列举真实世界的拜占庭故障案例，并展示为什么像 Raft 这样的崩溃容错算法无法应对这类故障。

## 题目说明

什么是拜占庭故障（Byzantine Fault）？与崩溃故障（Crash Fault）不同，崩溃故障只是节点停止工作、不再响应，而拜占庭故障允许节点做出任意的异常行为。一个出现拜占庭故障的节点可能会撒谎、向不同的节点发送互相矛盾的消息、或者选择性地只与部分节点通信。

请列举 3 个真实世界中的拜占庭故障案例，并展示为什么崩溃容错算法无法应对：

```json
Request:  {"type": "classify_fault", "msg_id": 1, "scenario": "node_sends_different_values_to_different_peers"}
Response: {"type": "classify_fault_ok", "in_reply_to": 1, "fault_type": "byzantine", "cft_handles": false, "bft_handles": true, "example": "equivocation attack"}

Request:  {"type": "byzantine_examples", "msg_id": 2}
Response: {"type": "byzantine_examples_ok", "in_reply_to": 2, "examples": [
    {"name": "hardware_bit_flip", "description": "Memory corruption changes stored value silently", "fault_type": "byzantine"},
    {"name": "compromised_node", "description": "Attacker controls node, sends malicious messages", "fault_type": "byzantine"},
    {"name": "software_bug", "description": "Bug causes node to return wrong computation result", "fault_type": "byzantine"}
]}

Request:  {"type": "cft_failure_demo", "msg_id": 3, "algorithm": "raft", "byzantine_node": "n2", "behavior": "equivocation"}
Response: {"type": "cft_failure_demo_ok", "in_reply_to": 3, "consensus_reached": true, "value_correct": false, "reason": "raft_trusted_byzantine_node_response"}
```

## 概念说明

**拜占庭故障与崩溃故障的区别**：可以用"叛徒"来类比。崩溃故障就像一个士兵倒下不动了，大家很容易发现他不在了。而拜占庭故障就像一个叛徒，他会假装配合，但暗地里发出错误的指令，甚至向不同的同伴传达不同的信息。这种"内鬼"比"掉线"要危险得多。

**为什么崩溃容错算法不够用？** 像 Raft 和 Paxos 这样的算法假设节点要么正常工作、要么完全停机。它们无条件信任收到的消息内容，所以一旦有节点发送虚假消息，整个系统可能会得出错误的结论。

## 涉及概念

- `Byzantine fault`
- `crash fault`
- `malicious node`
- `bit flip`
- `CFT vs BFT`

## 实现提示

- 拜占庭节点可以表现出任意行为：撒谎、向不同节点发送不同消息等
- 崩溃故障是拜占庭故障的一个子集（崩溃等于沉默，不是说谎）
- 真实世界案例：硬件比特翻转导致数据悄悄变错、被入侵的节点发送恶意消息、软件缺陷导致返回错误的计算结果
- 崩溃容错算法（如 Raft、Paxos）无法应对拜占庭故障
- 拜占庭容错要求至少 `N >= 3f+1` 个节点才能容忍 `f` 个拜占庭故障节点

## 测试用例

### 1. 将"说谎"行为分类为拜占庭故障

验证说明：一个节点向不同的伙伴发送不同的值，应被归类为拜占庭故障。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"classify_fault","msg_id":2,"scenario":"node_sends_different_values_to_different_peers"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "classify_fault_ok", "in_reply_to": 2, "fault_type": "byzantine", "cft_handles": false, "bft_handles": true, "msg_id": 1}}
```

### 2. 列出拜占庭故障的实例

验证说明：响应中应包含至少 3 个示例，且所有示例的 `fault_type` 都为 `"byzantine"`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"byzantine_examples","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [The Byzantine Generals Problem - Lamport](https://lamport.azurewebsites.net/pubs/byz.pdf)：定义拜占庭故障模型的原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
