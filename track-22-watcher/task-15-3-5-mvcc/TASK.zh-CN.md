# 实现 etcd 的多版本并发控制键值存储

英文标题：Implement etcd MVCC for Versioned Key-Value Store
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-5-mvcc>

课程：22. 观察者
任务序号：15
短标题：etcd MVCC
难度：高级
子主题：一致性与 ZAB 协议

## 中文导读

这道题要求你实现 etcd 的多版本并发控制机制。普通的键值存储每次写入都会覆盖旧值，而多版本并发控制会把每个键的所有历史版本都保留下来。你可以把它想象成给数据装了一台"时光机"：不仅能读取最新值，还能回到任意历史时刻查看当时的数据。这个特性对监听器尤其重要——即使监听器暂时断开连接，重连后也能从断点处追赶上来，不会丢失任何变更。当然，无限保留历史版本会耗尽存储空间，所以还需要实现压缩操作来定期清理旧版本。

## 题目说明

etcd 采用多版本并发控制（MVCC）来存储数据，即保留每个键的所有历史版本。这样做带来两大好处：一是支持历史读取，二是让监听器能够安全地追赶进度。

具体工作原理如下：

1. 系统维护一个全局修订号（Revision）计数器，每次有任何键被修改，计数器就加一
2. 执行 `Put("/config", "v1")` 时，值 "v1" 被记录在当前修订号（比如 42）下
3. 再执行 `Put("/config", "v2")` 时，值 "v2" 被记录在下一个修订号（43）下，而修订号 42 对应的 "v1" 仍然保留
4. 执行 `Get("/config")` 默认返回最新版本，即修订号 43 处的 "v2"
5. 执行 `Get("/config", revision=42)` 则返回历史版本，即修订号 42 处的 "v1"

关于压缩（Compaction）：随着数据不断写入，历史版本会越积越多。压缩操作用于释放空间，例如 `Compact(revision=40)` 会删除修订号 40 之前的所有历史版本。此后，任何针对修订号 40 之前的历史读取都会失败。

关于监听器安全性：假设一个监听器当前进度在修订号 42，即使它暂时断开连接，重连后只需请求修订号 42 之后的变更即可完整追赶。只要这些修订号还没有被压缩掉，就不会丢失任何数据。

协议示例：

```json
Request:  {"type": "etcd_put", "msg_id": 1, "key": "/cfg", "value": "v1"}
Response: {"type": "etcd_put_ok", "in_reply_to": 1, "revision": 1}

Request:  {"type": "etcd_get", "msg_id": 2, "key": "/cfg", "revision": 1}
Response: {"type": "etcd_get_ok", "in_reply_to": 2, "key": "/cfg", "value": "v1", "mod_revision": 1}

Request:  {"type": "etcd_compact", "msg_id": 3, "revision": 5}
Response: {"type": "etcd_compact_ok", "in_reply_to": 3, "compacted_to": 5, "versions_removed": 12}
```

## 涉及概念

- `MVCC`
- `multi-version concurrency`
- `revision`
- `compaction`
- `historical reads`

## 实现提示

- 每个键可以有多个版本，由全局修订号计数器统一编排
- 写入操作先递增全局修订号，再将键值对存储在该修订号下
- 读取时指定修订号可以获取历史版本的数据
- 压缩操作删除指定修订号之前的所有历史版本，释放存储空间
- 多版本并发控制使得监听器即使暂时落后也能安全追赶：只需从已知的修订号开始请求后续变更即可

## 测试用例

### 1. 历史读取返回旧版本

验证说明：对同一个键写入两次后，指定修订号 1 进行读取时应返回第一次写入的值 "v1"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/k","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":3,"key":"/k","value":"v2"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_get","msg_id":4,"key":"/k","revision":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 压缩操作清理旧版本

验证说明：压缩结果应包含压缩到的修订号以及被清理的版本数量。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_compact","msg_id":2,"revision":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [etcd MVCC](https://etcd.io/docs/v3.5/learning/data_model/)：etcd 官方文档中关于多版本并发控制数据模型和基于修订号的版本管理的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
