# 构建 Leader 选举，包含ZooKeeper

英文标题：Build Leader Election，包含ZooKeeper
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-4-leader-election>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：9
短标题：Leader 选举
难度：advanced
子主题：Watches和Sessions

## 中文导读

本题要求你完成 `构建 Leader 选举，包含ZooKeeper`。

重点关注：`leader election`、`ephemeral sequential`、`smallest number wins`、`watch predecessor`、`automatic re-election`。

建议先按提示逐步实现：Each Candidate creates an ephemeral sequential 节点 under /election。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Leader election in ZooKeeper uses ephemeral sequential 节点. Each Candidate creates a 节点,和the one，包含the lowest sequence number is the Leader.

**Election algorithm**:
1. Each Candidate creates: `/election/Candidate-` (EPHEMERAL + SEQUENTIAL)
2. Get all children of `/election`和sort by sequence number
3. If your 节点 has the lowest number, you are the **Leader**
4. Otherwise, watch the 节点 immediately before yours
5. If the Leader crashes, its ephemeral 节点 is deleted
6. The next Candidate's watch fires,和it checks if it is now the lowest

**Automatic re-election**: because 节点 are ephemeral, Leader 故障 triggers automatic deletion, which triggers the next Candidate's watch, causing seamless failover.

```JSON
请求:  {"type": "election_join", "msg_id": 1, "path": "/election", "Candidate": "n1", "session_id": "s1"}
响应: {"type": "election_join_ok", "in_reply_to": 1, "节点": "/election/Candidate-0000000001", "is_leader": true, "Leader": "n1"}

请求:  {"type": "election_status", "msg_id": 2, "path": "/election"}
响应: {"type": "election_status_ok", "in_reply_to": 2, "Leader": "n1", "candidates": ["n1", "n2", "n3"], "ordered_nodes": ["/election/Candidate-0000000001", "/election/Candidate-0000000002", "/election/Candidate-0000000003"]}
```

## 涉及概念

- `leader election`
- `ephemeral sequential`
- `smallest number wins`
- `watch predecessor`
- `automatic re-election`

## 实现提示

- Each Candidate creates an ephemeral sequential 节点 under /election
- The 节点，包含the lowest sequence number is the Leader
- Other candidates watch the 节点 immediately before them
- If the Leader crashes, its ephemeral 节点 is deleted, triggering re-election
- The next-lowest numbered 节点 automatically becomes the new Leader

## 测试用例

### 1. First candidate becomes Leader

election_join_ok should show is_leader: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"election_join","msg_id":2,"path":"/election","candidate":"n1","session_id":"s1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Second candidate is follower

Second join should show is_leader: false和Leader: "n1".

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

- [ZooKeeper Leader Election](https://zookeeper.apache.org/doc/current/recipes.html#sc_leaderElection)：ZooKeeper documentation on the Leader election recipe

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
