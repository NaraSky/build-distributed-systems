# 实现 Sequential Nodes用于Ordering

英文标题：Implement Sequential Nodes用于Ordering
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-5-sequential>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：5
短标题：Sequential Nodes
难度：intermediate
子主题：The ZNode Data模式l

## 中文导读

本题要求你完成 `实现 Sequential Nodes用于Ordering`。

重点关注：`sequential node`、`auto-incrementing`、`distributed queue`、`leader election`、`ordering guarantee`。

建议先按提示逐步实现：Create("/election/Candidate-", ..., SEQUENTIAL) produces /election/Candidate-0000000001。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Sequential 节点 have a unique, auto-incremented 10-digit suffix appended by ZooKeeper. They guarantee ordering even when multiple clients create concurrently.

**How it works**:
1. 客户端 sends `Create("/election/Candidate-", data, SEQUENTIAL)`
2. ZooKeeper appends a 10-digit monotonically increasing number
3. Result: `/election/Candidate-0000000001`
4. Next create: `/election/Candidate-0000000002`

**Use cases**:
- **Leader election**: each Candidate creates a sequential ephemeral 节点. The lowest number is the Leader.
- **Distributed 队列**: producers create sequential 节点 (enqueue), consumers process the lowest number (dequeue).
- **Barriers**: N processes create sequential 节点; when N 节点 exist, the barrier is released.

```JSON
请求:  {"type": "znode_create", "msg_id": 1, "path": "/election/Candidate-", "data": "n1", "ephemeral": true, "sequential": true, "session_id": "s1"}
响应: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/election/Candidate-0000000001", "version": 0}

请求:  {"type": "znode_create", "msg_id": 2, "path": "/election/Candidate-", "data": "n2", "ephemeral": true, "sequential": true, "session_id": "s2"}
响应: {"type": "znode_create_ok", "in_reply_to": 2, "path": "/election/Candidate-0000000002", "version": 0}
```

## 涉及概念

- `sequential node`
- `auto-incrementing`
- `distributed queue`
- `leader election`
- `ordering guarantee`

## 实现提示

- Create("/election/Candidate-", ..., SEQUENTIAL) produces /election/Candidate-0000000001
- The 10-digit suffix is monotonically increasing (global 计数器 per parent)
- Sequential 节点 guarantee a unique, ordered name even，包含concurrent creates
- Use case: distributed 队列 — enqueue creates sequential, dequeue processes lowest
- Use case: Leader election — lowest sequence number is the Leader

## 测试用例

### 1. Sequential creates get increasing suffixes

Second path suffix should be greater than first.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/q/item-","data":"a","ephemeral":false,"sequential":true}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":3,"path":"/q/item-","data":"b","ephemeral":false,"sequential":true}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Sequential names are 唯一

Both created paths should be different (unique suffixes).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/s/n-","data":"","ephemeral":false,"sequential":true}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":3,"path":"/s/n-","data":"","ephemeral":false,"sequential":true}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Sequential Nodes](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#Sequence+Nodes+--+Unique+Naming)：ZooKeeper documentation on sequential 节点和unique naming

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
