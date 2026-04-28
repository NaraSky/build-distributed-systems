# 实现顺序节点以保证排序

英文标题：Implement Sequential Nodes for Ordering
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-5-sequential>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：5
短标题：Sequential Nodes
难度：进阶
子主题：The ZNode Data Model

## 中文导读

这道题要求你实现顺序节点（Sequential Node）。顺序节点的特点是 ZooKeeper 会自动在节点名后面追加一个 10 位的递增数字。即使多个客户端同时创建，也能保证每个节点有唯一的序号。这个特性是实现分布式锁和领导者选举等高级功能的关键基石。

## 题目说明

顺序节点（Sequential Node）由 ZooKeeper 自动追加一个唯一的 10 位递增后缀。即使多个客户端并发创建，也能保证顺序。

**工作原理**：
1. 客户端发送 `Create("/election/candidate-", data, SEQUENTIAL)`
2. ZooKeeper 追加一个 10 位的单调递增数字
3. 结果：`/election/candidate-0000000001`
4. 下次创建：`/election/candidate-0000000002`

**典型用例**：
- **领导者选举**：每个候选者创建一个顺序临时节点，序号最小的就是领导者。
- **分布式队列**：生产者创建顺序节点（入队），消费者处理序号最小的（出队）。
- **屏障（Barrier）**：N 个进程各创建一个顺序节点；当节点数达到 N 时，屏障释放。

```json
Request:  {"type": "znode_create", "msg_id": 1, "path": "/election/candidate-", "data": "n1", "ephemeral": true, "sequential": true, "session_id": "s1"}
Response: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/election/candidate-0000000001", "version": 0}

Request:  {"type": "znode_create", "msg_id": 2, "path": "/election/candidate-", "data": "n2", "ephemeral": true, "sequential": true, "session_id": "s2"}
Response: {"type": "znode_create_ok", "in_reply_to": 2, "path": "/election/candidate-0000000002", "version": 0}
```

## 涉及概念

- `sequential node`
- `auto-incrementing`
- `distributed queue`
- `leader election`
- `ordering guarantee`

## 实现提示

- Create("/election/candidate-", ..., SEQUENTIAL) 会生成 /election/candidate-0000000001
- 10 位后缀单调递增（每个父节点维护一个全局计数器）
- 顺序节点保证即使并发创建也能获得唯一且有序的名称
- 分布式队列用例：入队时创建顺序节点，出队时处理序号最小的
- 领导者选举用例：序号最小的节点就是领导者

## 测试用例

### 1. 连续创建获得递增的后缀

第二个路径的后缀应当大于第一个。

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

### 2. 顺序节点的名称唯一

两个创建的路径应当不同（后缀唯一）。

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

- [ZooKeeper Sequential Nodes](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#Sequence+Nodes+--+Unique+Naming)：ZooKeeper 关于顺序节点和唯一命名的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
