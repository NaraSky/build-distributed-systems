# 基于 ZooKeeper 实现领导者选举

英文标题：Build Leader Election with ZooKeeper
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-4-leader-election>

课程：22. 观察者
任务序号：9
短标题：Leader Election
难度：高级
子主题：监听与会话

## 中文导读

这道题要求你利用临时顺序节点（Ephemeral Sequential Node）实现领导者选举。核心思路非常直观：每个候选者在同一个目录下创建一个带自增编号的临时节点，编号最小的那个就是领导者。由于节点是临时的，一旦领导者崩溃或断开连接，它的节点会自动消失，编号排在它后面的候选者立刻感知到变化并接替领导权，实现完全自动的故障转移。

## 题目说明

ZooKeeper 中的领导者选举（Leader Election）利用临时顺序节点来实现。每个候选者创建一个节点，编号最小的自动成为领导者。

选举算法的具体步骤如下：

1. 每个候选者在 `/election` 目录下创建一个临时顺序节点，例如 `/election/candidate-0000000001`
2. 获取 `/election` 下的所有子节点，按序列号从小到大排序
3. 如果自己创建的节点序号最小，那么自己就是领导者
4. 如果不是最小的，就监听排在自己前面的那个节点（而不是监听领导者节点，这样可以避免"惊群效应"）
5. 当领导者崩溃时，它的临时节点会被系统自动删除
6. 排在它后面的候选者会收到监听通知，然后检查自己是否变成了序号最小的节点

这个机制的精妙之处在于：由于节点是临时的，领导者故障会自动触发节点删除，进而触发下一位候选者的监听器，整个故障转移过程完全自动，无需人工干预。

协议示例：

```json
Request:  {"type": "election_join", "msg_id": 1, "path": "/election", "candidate": "n1", "session_id": "s1"}
Response: {"type": "election_join_ok", "in_reply_to": 1, "node": "/election/candidate-0000000001", "is_leader": true, "leader": "n1"}

Request:  {"type": "election_status", "msg_id": 2, "path": "/election"}
Response: {"type": "election_status_ok", "in_reply_to": 2, "leader": "n1", "candidates": ["n1", "n2", "n3"], "ordered_nodes": ["/election/candidate-0000000001", "/election/candidate-0000000002", "/election/candidate-0000000003"]}
```

## 涉及概念

- `leader election`
- `ephemeral sequential`
- `smallest number wins`
- `watch predecessor`
- `automatic re-election`

## 实现提示

- 每个候选者在选举目录下创建一个临时顺序节点
- 序号最小的节点对应的候选者就是领导者
- 其他候选者只需监听排在自己紧前面的那个节点，而非直接监听领导者
- 当领导者崩溃时，其临时节点自动删除，后续候选者依次收到通知并重新判定
- 序号次小的节点自动成为新的领导者，无需重新创建节点

## 测试用例

### 1. 第一个候选者成为领导者

验证说明：第一个加入选举的候选者应当直接成为领导者。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"election_join","msg_id":2,"path":"/election","candidate":"n1","session_id":"s1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 第二个候选者成为跟随者

验证说明：第二个加入的候选者不是领导者，且返回结果中显示当前领导者为 "n1"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"election_join","msg_id":2,"path":"/election","candidate":"n1","session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"election_join","msg_id":3,"path":"/election","candidate":"n2","session_id":"s2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Leader Election](https://zookeeper.apache.org/doc/current/recipes.html#sc_leaderElection)：ZooKeeper 官方文档中关于领导者选举方案的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
