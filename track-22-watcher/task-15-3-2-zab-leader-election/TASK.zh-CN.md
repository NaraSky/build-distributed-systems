# 实现 ZAB Leader 选举，包含FastLeaderElection

英文标题：Implement ZAB Leader Election，包含FastLeaderElection
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-2-zab-leader-election>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：12
短标题：ZAB 选举
难度：advanced
子主题：Consistency和the ZAB Protocol

## 中文导读

本题要求你完成 `实现 ZAB Leader 选举，包含FastLeaderElection`。

重点关注：`ZAB leader election`、`FastLeaderElection`、`zxid comparison`、`epoch`、`voting rounds`。

建议先按提示逐步实现：The 服务端，包含the highest zxid (most up-to-date 日志) wins the election。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

ZAB Leader election selects the 服务端，包含the most up-to-date 事务 日志 (highest `zxid`) as the new Leader. This minimizes data synchronization after election.

**FastLeaderElection algorithm**:
1. Each 服务端 starts by voting用于itself: `(myId, myZxid)`
2. Servers exchange votes. If a received vote has a higher zxid (or higher 服务端 ID as tiebreaker), update your vote to match.
3. Continue until a quorum (majority) of servers all vote用于the same Candidate.
4. The elected Leader enters the **synchronization phase**: sends missing proposals to followers.
5. After synchronization, the Leader begins serving requests.

**Epoch**: each new Leader increments the epoch (upper 32 bits of zxid). This fences stale leaders.

```JSON
请求:  {"type": "zab_election", "msg_id": 1}
响应: {"type": "zab_election_ok", "in_reply_to": 1, "Leader": "n2", "leader_zxid": "0x200000005", "epoch": 2, "rounds": 3, "votes_received": {"n1": "n2", "n2": "n2", "n3": "n2"}}
```

## 涉及概念

- `ZAB leader election`
- `FastLeaderElection`
- `zxid comparison`
- `epoch`
- `voting rounds`

## 实现提示

- The 服务端，包含the highest zxid (most up-to-date 日志) wins the election
- FastLeaderElection: each 服务端 proposes itself, then updates its vote to the 服务端，包含the highest zxid
- Voting continues in rounds until a quorum agrees on the same Candidate
- After election, the Leader synchronizes followers (sends missing proposals)
- The epoch increments on each new Leader to fence stale leaders

## 测试用例

### 1. 选举 produces a Leader

zab_election_ok should include Leader, leader_zxid, epoch,和votes_received.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_election","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Quorum votes用于same Leader

A majority of votes_received values should match the Leader.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_election","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZAB Leader Election](https://zookeeper.apache.org/doc/current/zookeeperInternals.html#sc_leaderElection)：ZooKeeper documentation on FastLeaderElection algorithm

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
