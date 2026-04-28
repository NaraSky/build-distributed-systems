# 实现 ZAB Atomic 广播 Protocol

英文标题：Implement ZAB Atomic Broadcast Protocol
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-1-zab>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：11
短标题：ZAB 广播
难度：advanced
子主题：Consistency和the ZAB Protocol

## 中文导读

本题要求你完成 `实现 ZAB Atomic 广播 Protocol`。

重点关注：`ZAB`、`atomic broadcast`、`2-phase commit`、`proposal`、`quorum acknowledgement`。

建议先按提示逐步实现：Leader receives a write 请求和creates a proposal，包含a unique zxid。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

ZAB (ZooKeeper Atomic 广播) is the 共识 protocol that keeps all ZooKeeper servers in sync. It guarantees that all servers see updates in the same order.

**ZAB 2-phase protocol**:
1. **Propose**: Leader assigns a monotonically increasing `zxid` to the update和broadcasts a PROPOSAL to all followers
2. **ACK**: each Follower writes the proposal to its WAL和sends an ACK to the Leader
3. **Commit**: when the Leader receives ACKs from a **quorum** (majority), it broadcasts COMMIT
4. **Apply**: each Follower (and the Leader) applies the committed update to the in-memory ZNode tree

**Ordering guarantee**: because `zxid` is monotonically increasing和proposals are applied in order, all servers see the same sequence of updates (sequential consistency).

```JSON
请求:  {"type": "zab_propose", "msg_id": 1, "operation": "SetData", "path": "/config", "data": "v2", "zxid": "0x100000001"}
响应: {"type": "zab_propose_ok", "in_reply_to": 1, "acks_received": 2, "quorum_size": 2, "committed": true}
```

## 涉及概念

- `ZAB`
- `atomic broadcast`
- `2-phase commit`
- `proposal`
- `quorum acknowledgement`

## 实现提示

- Leader receives a write 请求和creates a proposal，包含a unique zxid
- Leader broadcasts the proposal to all followers
- Followers write the proposal to their local WAL和send ACK to the Leader
- When the Leader receives ACKs from a quorum (majority), it sends COMMIT
- Followers apply the committed proposal to their in-memory tree

## 测试用例

### 1. Proposal，包含quorum commits

zab_propose_ok should show committed: true when acks >= quorum.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":2,"operation":"SetData","path":"/cfg","data":"v1","zxid":"0x100000001"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Sequential zxids are ordered

Both proposals should commit in zxid order.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":2,"operation":"SetData","path":"/a","data":"1","zxid":"0x100000001"}}
{"src":"c1","dest":"n1","body":{"type":"zab_propose","msg_id":3,"operation":"SetData","path":"/b","data":"2","zxid":"0x100000002"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZAB Protocol](https://zookeeper.apache.org/doc/current/zookeeperInternals.html#sc_atomicBroadcast)：ZooKeeper documentation on Atomic 广播 protocol

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
