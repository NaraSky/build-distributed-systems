# 实现兼容 etcd 的 API 层

英文标题：Implement an etcd-Compatible API Layer
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-4-etcd-api>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：14
短标题：etcd API
难度：高级
子主题：Consistency and the ZAB Protocol

## 中文导读

这道题要求你在已有的 ZAB 共识层之上实现一套兼容 etcd 的键值 API。etcd 是 Kubernetes 的核心存储组件，它的 API 风格与 ZooKeeper 不同：扁平的键值对而非树形结构，持久监听而非一次性监听，以及强大的事务操作。通过这道题你会理解，同样的共识基础可以支撑不同风格的上层接口。

## 题目说明

etcd 在基于 Raft 的共识层之上提供了一套现代化的键值 API。在你的 ZAB 系统上实现兼容 etcd 的 API，可以展示同样的协调原语如何支撑不同的接口。

**核心 API**：
- `Put(key, value)`：存储一个键值对
- `Get(key)`：获取最新的值及其修订号
- `Delete(key)`：删除一个键
- `Txn(compare, success, failure)`：原子事务，如果 compare 条件成立则执行 success 操作，否则执行 failure 操作
- `Watch(key)`：持久监听（与 ZooKeeper 的一次性监听不同）

**事务示例**（比较并交换）：
```
Txn: if value("/leader") == "n1", then Put("/leader", "n2"), else fail
```

```json
Request:  {"type": "etcd_put", "msg_id": 1, "key": "/config/db_host", "value": "10.0.0.5"}
Response: {"type": "etcd_put_ok", "in_reply_to": 1, "revision": 42}

Request:  {"type": "etcd_txn", "msg_id": 2, "compare": {"key": "/leader", "value": "n1"}, "success": [{"op": "put", "key": "/leader", "value": "n2"}], "failure": []}
Response: {"type": "etcd_txn_ok", "in_reply_to": 2, "succeeded": true, "revision": 43}
```

## 涉及概念

- `etcd API`
- `Get`
- `Put`
- `Delete`
- `Txn`
- `compare-and-swap`

## 实现提示

- etcd 提供扁平的键值 API（没有像 ZooKeeper 那样的层级结构）
- 事务操作实现原子的比较并交换：如果条件成立则执行操作，否则执行其他操作
- 监听是持久的（与 ZooKeeper 的一次性监听不同）
- 每次修改都会递增一个全局修订号计数器
- 在你已有的共识层之上实现即可

## 测试用例

### 1. Put 和 Get 的往返测试

etcd_get_ok 应当返回 value 为 "v1"，且 revision > 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/k1","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_get","msg_id":3,"key":"/k1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 条件匹配时事务成功

etcd_txn_ok 应当显示 succeeded: true。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/l","value":"n1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_txn","msg_id":3,"compare":{"key":"/l","value":"n1"},"success":[{"op":"put","key":"/l","value":"n2"}],"failure":[]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [etcd API](https://etcd.io/docs/v3.5/learning/api/)：etcd 关于键值 API 和事务操作的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
