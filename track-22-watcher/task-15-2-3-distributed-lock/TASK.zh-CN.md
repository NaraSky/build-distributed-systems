# 基于 ZooKeeper 原语构建分布式锁

英文标题：Build a Distributed Lock with ZooKeeper Primitives
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-3-distributed-lock>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：8
短标题：Distributed Lock
难度：高级
子主题：Watches and Sessions

## 中文导读

这道题要求你用 ZooKeeper 的临时顺序节点来实现分布式锁。核心思路是：每个想获取锁的客户端创建一个临时顺序节点，序号最小的获得锁。巧妙之处在于，等待的客户端只监听它前面那个节点，而不是锁持有者，这样锁释放时只会通知一个客户端，避免了"惊群效应"。

## 题目说明

使用 ZooKeeper 构建分布式锁，利用临时顺序节点（Ephemeral Sequential Node）创建一种公平、无死锁的加锁机制。

**加锁算法**（避免"惊群效应"）：
1. 创建一个临时顺序节点：`/locks/lock-` -> `/locks/lock-0000000005`
2. 获取 `/locks` 的所有子节点，按序号排序
3. 如果你的节点序号**最小**，你就持有了锁。结束。
4. 否则，监听排在你**前面**的那个节点
5. 当那个节点被删除（前驱释放了锁），重新检查第 3 步
6. 释放锁：直接删除你的节点（如果客户端崩溃，临时节点会自动超时删除）

**为什么只监听前驱节点？** 如果所有等待者都监听锁持有者，锁一释放就会触发 N 个监听事件（惊群效应）。只监听前驱节点意味着每次只通知一个客户端。

```json
Request:  {"type": "lock_acquire", "msg_id": 1, "lock_path": "/locks/my-lock", "session_id": "s1"}
Response: {"type": "lock_acquire_ok", "in_reply_to": 1, "lock_node": "/locks/my-lock/lock-0000000001", "acquired": true, "position": 1}

Request:  {"type": "lock_release", "msg_id": 2, "lock_node": "/locks/my-lock/lock-0000000001"}
Response: {"type": "lock_release_ok", "in_reply_to": 2, "released": true}
```

## 涉及概念

- `distributed lock`
- `ephemeral sequential`
- `herd effect`
- `watch predecessor`
- `fair locking`

## 实现提示

- 在 /locks 下创建一个临时顺序节点：/locks/lock-0000000001
- 获取 /locks 的所有子节点并按序号排序
- 如果你的节点序号最小，你就持有了锁
- 否则，监听排在你前面的那个节点（避免惊群效应）
- 当那个节点被删除（锁释放），重新检查你是否已经是序号最小的

## 测试用例

### 1. 无竞争时获取锁

lock_acquire_ok 应当显示 acquired: true 和 position: 1。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_acquire","msg_id":2,"lock_path":"/locks/l1","session_id":"s1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 第二个请求者在队列中等待

第一个应当显示 acquired: true，第二个应当显示 acquired: false 且 position: 2。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_acquire","msg_id":2,"lock_path":"/locks/l2","session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"lock_acquire","msg_id":3,"lock_path":"/locks/l2","session_id":"s2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Lock Recipe](https://zookeeper.apache.org/doc/current/recipes.html#sc_recipes_Locks)：ZooKeeper 关于分布式锁实现方案的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
