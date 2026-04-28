# 通过任期管理防止选票瓜分

网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-5-split-vote>

课程：5. 选举器：领导者选举
任务序号：5
短标题：任期管理
难度：高级
子主题：Raft 领导者选举

## 中文导读

这道题让你处理选票瓜分的情况：没有任何候选人获得多数票。此时候选人需要递增任期号并重新发起选举。正确的任期管理能确保集群最终选出领导者。任期号就像一个逻辑时钟，是 Raft 判断信息新旧的核心依据。

## 题目说明

处理选票瓜分（Split Vote）的情况，即没有候选人获得多数票。候选人递增自己的任期号并重新发起选举。正确的任期管理能确保集群最终选出一个领导者。

## 概念说明

### 任期管理

任期号（Term）相当于一个逻辑时钟。更高的任期号总是优先。当一个节点看到比自己更高的任期号时，它会立即退回到跟随者状态。这可以防止过时的领导者造成不一致。就像朝代更替：一旦新朝代建立（更高的任期号），旧朝代的命令就不再有效，所有人都必须服从新朝代。

## 涉及概念

- `term`
- `split vote`
- `election retry`

## 实现提示

- 发起选举时递增任期号
- 如果看到更高的任期号，立即退回跟随者状态
- 选举超时后重新发起选举

## 测试用例

### 1. 发起新选举时递增任期号

节点在发起选举时将任期号从 1 递增到 2，变成候选人，并给自己投票。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"set_term","msg_id":2,"term":1}}
{"src":"c0","dest":"n1","body":{"type":"trigger_election_timeout","msg_id":3}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":4}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"trigger_election_timeout_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":4,"msg_id":3,"state":"candidate","term":2}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
