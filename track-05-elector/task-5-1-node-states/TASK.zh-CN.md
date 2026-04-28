# 实现节点状态：领导者、跟随者、候选人

网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-1-node-states>

课程：5. 选举器：领导者选举
任务序号：1
短标题：节点状态
难度：进阶
子主题：Raft 领导者选举

## 中文导读

这道题让你实现 Raft 协议中的三种节点状态：领导者、跟随者和候选人。这是 Raft 领导者选举的基础，理解这三种状态之间的转换关系，是理解整个 Raft 协议的第一步。每个节点启动时都是跟随者，只有通过选举才能成为领导者。

## 题目说明

实现 Raft 协议中的三种状态：领导者（Leader）、跟随者（Follower）和候选人（Candidate）。每个节点启动时处于跟随者状态。候选人向其他节点请求投票。领导者负责协调整个集群。

## 概念说明

### Raft 角色

在 Raft 协议中，每个节点始终处于三种状态之一：跟随者（被动响应领导者的请求）、候选人（正在竞选成为领导者）或领导者（处理所有客户端请求）。这种清晰的状态机设计大大简化了对协议的理解和推理。可以类比为一个团队：平时大家都是普通成员（跟随者），需要选队长时有人站出来竞选（候选人），选上了就是队长（领导者）。

## 涉及概念

- `state machine`
- `leader election`
- `Raft roles`

## 实现提示

- 定义一个枚举类型来表示三种状态
- 所有节点启动时都是跟随者
- 状态转换在特定事件发生时触发

## 测试用例

### 1. 节点启动时为跟随者状态

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":2}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":2,"msg_id":1,"state":"follower","term":0}}
```

## 参考资料

- [Raft Paper](https://raft.github.io/raft.pdf)：Raft 论文，寻找一种易于理解的共识算法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
