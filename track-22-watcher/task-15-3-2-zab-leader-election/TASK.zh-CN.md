# 实现 ZAB 领导者选举与快速选举算法

英文标题：Implement ZAB Leader Election with FastLeaderElection
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-2-zab-leader-election>

课程：22. 观察者
任务序号：12
短标题：ZAB Election
难度：高级
子主题：一致性与 ZAB 协议

## 中文导读

这道题要求你实现 ZAB 协议中的领导者选举机制。和上一题中基于顺序节点的客户端选举不同，这里是 ZooKeeper 集群内部服务器之间的选举。核心原则是"数据最新者优先"：谁的事务日志最新（即事务编号最大），谁就最有资格当领导者。这样做的好处是选举结束后，新领导者需要同步给跟随者的数据量最少，集群恢复速度最快。

## 题目说明

ZAB 的领导者选举会选出事务日志最新的服务器（即事务编号最高的那台）作为新领导者。这种策略能最大限度地减少选举后的数据同步开销。

快速选举算法（FastLeaderElection）的流程如下：

1. 每台服务器启动时先投票给自己，投票内容是 `(自己的编号, 自己的最新事务编号)`
2. 服务器之间互相交换投票。如果收到的投票中事务编号比自己的高，或者事务编号相同但服务器编号更大（作为平局决胜条件），就把自己的投票改为对方的选择
3. 经过若干轮交换，当超过半数的服务器都投给同一个候选者时，选举结束
4. 当选的领导者进入同步阶段，将跟随者缺少的提案发送给它们
5. 同步完成后，领导者开始正常对外提供服务

关于纪元（Epoch）：每当产生新的领导者，纪元号就会递增。纪元号存储在事务编号的高 32 位中。它的作用是隔离过期的旧领导者——如果一个旧领导者在网络分区后恢复，它的纪元号比当前领导者低，所有服务器都会拒绝它的请求。

协议示例：

```json
Request:  {"type": "zab_election", "msg_id": 1}
Response: {"type": "zab_election_ok", "in_reply_to": 1, "leader": "n2", "leader_zxid": "0x200000005", "epoch": 2, "rounds": 3, "votes_received": {"n1": "n2", "n2": "n2", "n3": "n2"}}
```

## 涉及概念

- `ZAB leader election`
- `FastLeaderElection`
- `zxid comparison`
- `epoch`
- `voting rounds`

## 实现提示

- 事务编号最高（即日志最新）的服务器优先当选
- 快速选举算法中，每台服务器先提名自己，然后在每一轮中将票投给事务编号最高的候选者
- 投票以轮次进行，直到超过半数的服务器达成一致
- 选举结束后，领导者需要先同步跟随者，把它们缺失的提案补齐
- 每次产生新领导者都要递增纪元号，用来拒绝旧领导者的过期请求

## 测试用例

### 1. 选举成功产生领导者

验证说明：选举结果应包含领导者标识、事务编号、纪元号以及各服务器的投票记录。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_election","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 多数服务器投票给同一个领导者

验证说明：在投票记录中，超过半数的服务器应当投给同一个候选者，且该候选者与返回的领导者一致。

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

- [ZAB Leader Election](https://zookeeper.apache.org/doc/current/zookeeperInternals.html#sc_leaderElection)：ZooKeeper 官方文档中关于快速选举算法的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
