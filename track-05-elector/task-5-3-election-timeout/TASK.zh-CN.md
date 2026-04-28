# 实现随机化选举超时

网页：<https://builddistributedsystem.com/tracks/elector/tasks/task-5-3-election-timeout>

课程：5. 选举器：领导者选举
任务序号：3
短标题：选举超时
难度：进阶
子主题：Raft 领导者选举

## 中文导读

这道题让你实现随机化的选举超时机制。当跟随者在超时时间内没有收到领导者的心跳，就会变成候选人发起选举。关键在于每个节点的超时时间是随机的，这样可以避免多个节点同时发起选举、互相"抢票"而选不出领导者的情况。

## 题目说明

添加随机化的选举超时机制。当跟随者在超时时间内没有收到领导者的消息时，它会变成候选人发起选举。使用随机化的超时时间，可以防止多个节点同时发起选举。

## 概念说明

### 随机化超时

如果所有节点使用相同的超时时间，网络波动可能导致多个节点同时发起选举，选票被瓜分，迟迟选不出领导者。打个比方，如果会议上所有人同时开口说话，谁的话也听不清。而随机化超时让各个节点在不同的时刻发起选举，通常只有一个节点最先超时并赢得选举，大大提高了选举效率。

## 涉及概念

- `randomization`
- `timeout`
- `split brain prevention`

## 实现提示

- 使用 150 到 300 毫秒之间的随机超时时间
- 收到心跳时重置超时计时器
- 不同的超时时间可以减少选票瓜分的情况

## 测试用例

### 1. 随机超时在 150-300 毫秒范围内

每次响应都包含一个 timeout_ms 字段，值在 150-300 之间。由于随机化，多次查询返回的值应该不同。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":2}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":3}}
{"src":"c0","dest":"n1","body":{"type":"get_election_timeout","msg_id":4}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c0","body":{"type":"election_timeout_reply","in_reply_to":4,"msg_id":3}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
