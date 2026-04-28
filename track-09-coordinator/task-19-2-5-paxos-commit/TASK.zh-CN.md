# 实现 Paxos 提交协议

网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-5-paxos-commit>

课程：9. 协调器：分布式事务
任务序号：10
短标题：Paxos Commit
难度：高级
子主题：三阶段提交

## 中文导读

这道题要求你实现 Paxos 提交协议。传统的两阶段提交依赖一个单独的协调者，一旦协调者宕机，整个事务就会卡住。Paxos 提交用一组共识节点替代了这个单点协调者，每个参与者的提交决策都通过 Paxos 算法达成共识，从根本上消除了单点故障。代价是更高的延迟和消息复杂度，但换来了更强的容错能力。

## 题目说明

在两阶段提交（2PC）中，整个事务的命运掌握在单一协调者手中——如果协调者崩溃了，所有参与者就只能干等着，无法自行决定提交还是回滚。Paxos 提交（Paxos Commit）的思路是：用一组 Paxos 共识节点来替代这个单一协调者。

**架构设计**：
- 每个参与者（Participant）都有自己专属的 Paxos 实例，用来决定该参与者是"提交"还是"中止"
- 提议者（Proposer）向每个参与者对应的 Paxos 实例提议"提交"或"中止"
- 一旦某个值被 Paxos 选定，就不可撤销
- 不存在单一协调者的故障点——如果一个提议者崩溃了，其他提议者可以接手继续推进

**协议流程**：对于每个参与者，都要走一遍完整的 Paxos 两阶段流程：

```
对于每个参与者 P：
  第一阶段a（准备）：提议者 → 接受者：Prepare(1)
  第一阶段b（承诺）：接受者 → 提议者：Promise(1, 之前接受的值)
  第二阶段a（接受）：提议者 → 接受者：Accept(1, "commit")
  第二阶段b（已接受）：接受者 → 提议者：Accepted(1, "commit")
```

**示例流程**：
```json
Request:  {"type": "paxos_commit_begin", "msg_id": 1, "participants": ["p1", "p2", "p3"], "acceptors": ["a1", "a2", "a3"], "operations": [{"transfer": 100, "from": "a", "to": "b"}]}

// 为参与者 p1 的决策执行第一阶段：
{"type": "prepare", "msg_id": 2, "proposal_id": 1, "participant": "p1"}
{"type": "promise", "in_reply_to": 2, "acceptor": "a1", "proposal_id": 1, "accepted_value": null}
{"type": "promise", "in_reply_to": 2, "acceptor": "a2", "proposal_id": 1, "accepted_value": null}
{"type": "promise", "in_reply_to": 2, "acceptor": "a3", "proposal_id": 1, "accepted_value": null}

// 为参与者 p1 的决策执行第二阶段：
{"type": "accept", "msg_id": 3, "proposal_id": 1, "participant": "p1", "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a1", "proposal_id": 1, "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a2", "proposal_id": 1, "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a3", "proposal_id": 1, "value": "commit"}

// 对 p2、p3 重复同样的流程...
```

**相比两阶段提交和三阶段提交的优势**：
- 没有单一协调者的故障点
- 可以容忍任意提议者的崩溃，其他提议者随时可以接手重试
- 只要大多数接受者可用，协议就不会阻塞

**代价**：
- 延迟更高：每个参与者需要两轮网络往返
- 消息数量更多：每个参与者需要 4N 条消息（N 为接受者数量）
- 实现更加复杂

## 涉及概念

- Paxos commit
- consensus-based commit
- no single point of failure
- acceptors
- proposers
- learners

## 实现提示

- 用一组 Paxos 接受者替代单一协调者
- 每个参与者的投票由其专属的 Paxos 实例来决定
- 第一阶段（准备）：提议者从接受者获取承诺
- 第二阶段（接受）：提议者发送值，接受者在已承诺的前提下接受
- 没有单点故障：任何提议者都可以驱动协议继续推进

## 测试用例

### 1. 成功的 Paxos 提交

验证：所有参与者都应通过 Paxos 共识达成提交决策。

输入：

```json
{"src":"c0","dest":"paxos_coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"],"acceptors":["a1","a2","a3"]}}
{"src":"c1","dest":"paxos_coord","body":{"type":"paxos_commit_begin","msg_id":2,"participants":["p1","p2","p3"],"acceptors":["a1","a2","a3"],"operations":[{"transfer":100,"from":"a","to":"b"}]}}
```

期望输出：

```text
{"src": "paxos_coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 提议者崩溃后恢复

验证：新的提议者应该接管并完成所有参与者的 Paxos 轮次。

输入：

```json
{"src":"c0","dest":"paxos_coord","body":{"type":"init","msg_id":1,"participants":["p1","p2"],"acceptors":["a1","a2","a3"]}}
{"src":"c1","dest":"paxos_coord","body":{"type":"paxos_commit_begin","msg_id":2,"participants":["p1","p2"],"acceptors":["a1","a2","a3"],"operations":[{"transfer":100,"from":"a","to":"b"}],"crash_proposer_after":"prepare"}}
{"src":"c2","dest":"paxos_coord","body":{"type":"recover_proposer","msg_id":3}}
```

期望输出：

```text
{"src": "paxos_coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Paxos Made Simple](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2007-81.pdf)：Lamport 的 Paxos 原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
