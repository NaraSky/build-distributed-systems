# 构建 a Distributed Lock，包含ZooKeeper Primitives

英文标题：Build a Distributed Lock，包含ZooKeeper Primitives
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-3-distributed-lock>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：8
短标题：Distributed Lock
难度：advanced
子主题：Watches和Sessions

## 中文导读

本题要求你完成 `构建 a Distributed Lock，包含ZooKeeper Primitives`。

重点关注：`distributed lock`、`ephemeral sequential`、`herd effect`、`watch predecessor`、`fair locking`。

建议先按提示逐步实现：Create an ephemeral sequential 节点 under /locks: /locks/lock-0000000001。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Building a distributed lock，包含ZooKeeper uses ephemeral sequential 节点 to create a fair, deadlock-free locking mechanism.

**Lock algorithm** (avoids "herd effect"):
1. Create an ephemeral sequential 节点: `/locks/lock-` -> `/locks/lock-0000000005`
2. Get all children of `/locks`和sort by sequence number
3. If your 节点 has the **lowest** sequence number, you hold the lock. Done.
4. Otherwise, watch the 节点 **immediately before** yours in sorted order
5. When that 节点 is deleted (predecessor released the lock), re-check step 3
6. Release: simply delete your 节点 (or let the ephemeral 超时 handle it on crash)

**Why watch only the predecessor?** If all waiters watched the lock holder, a single release would trigger N watch events (herd effect). Watching only the predecessor means only ONE 客户端 is notified.

```JSON
请求:  {"type": "lock_acquire", "msg_id": 1, "lock_path": "/locks/my-lock", "session_id": "s1"}
响应: {"type": "lock_acquire_ok", "in_reply_to": 1, "lock_node": "/locks/my-lock/lock-0000000001", "acquired": true, "position": 1}

请求:  {"type": "lock_release", "msg_id": 2, "lock_node": "/locks/my-lock/lock-0000000001"}
响应: {"type": "lock_release_ok", "in_reply_to": 2, "released": true}
```

## 涉及概念

- `distributed lock`
- `ephemeral sequential`
- `herd effect`
- `watch predecessor`
- `fair locking`

## 实现提示

- Create an ephemeral sequential 节点 under /locks: /locks/lock-0000000001
- Get all children of /locks和sort them by sequence number
- If your 节点 has the lowest number, you hold the lock
- Otherwise, watch the 节点 immediately BEFORE yours (avoids herd effect)
- When that 节点 is deleted (lock released), re-check if you are now the lowest

## 测试用例

### 1. Acquire lock when no contention

lock_acquire_ok should show acquired: true和position: 1.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_acquire","msg_id":2,"lock_path":"/locks/l1","session_id":"s1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Second acquirer waits in 队列

First should show acquired: true, second should show acquired: false，包含position: 2.

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

- [ZooKeeper Lock Recipe](https://zookeeper.apache.org/doc/current/recipes.html#sc_recipes_Locks)：ZooKeeper documentation on the distributed lock recipe

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
